import fcntl
import io
import logging
import os
import shutil
import tempfile
import time

import ass
import chardet

LOGGER = logging.getLogger(__name__)


class LockedIO:
    def __init__(self, filename, mode='r', **kwargs):
        kwargs['mode'] = mode
        self._filename = filename
        self._kwargs = kwargs
        self._fileobj = None

    def __enter__(self):

        fil = io.open(self._filename, **self._kwargs)
        while True:
            fcntl.flock(fil, fcntl.LOCK_EX)
            filtest = io.open(self._filename, **self._kwargs)
            if os.path.sameopenfile(fil.fileno(), filtest.fileno()):
                filtest.close()
                self._fileobj = fil
                return fil

            fil.close()
            fil = filtest

    def __exit__(self, _exc_type, _exc_value, _traceback):
        fil = self._fileobj
        if fil:
            fil.close()


class AtomicWriter(LockedIO):
    def __init__(self, filename, mode='wb', **kwargs):
        super().__init__(filename, mode, **kwargs)
        self._atomicobj = None

    def __enter__(self):

        super().__enter__()
        atomicargs = dict(self._kwargs.items())
        atomicargs.update(
            dict(
                prefix=os.path.basename(self._filename),
                dir=os.path.dirname(self._filename),
                delete=False,
            )
        )
        tmp = self._atomicobj = tempfile.NamedTemporaryFile(**atomicargs)
        self._fileobj.seek(0)
        try:
            shutil.copyfileobj(self._fileobj, tmp.file)
        except io.UnsupportedOperation:
            pass
        return tmp.file

    def __exit__(self, _exc_type, _exc_value, _traceback):
        tmp = self._atomicobj
        if tmp:
            tmp.file.flush()
            os.fsync(tmp.file.fileno())
            tmpname = tmp.name
            tmp.close()
            shutil.copymode(self._filename, tmpname)
            try:
                os.rename(tmpname, self._filename)
            except OSError:
                if not os.path.exists(self._filename):
                    raise
                os.unlink(self._filename)
                os.rename(tmpname, self._filename)
        super().__exit__(_exc_type, _exc_value, _traceback)


def detect_file_encoding(filename):
    buffer = b''
    with io.open(filename, 'rb') as inp:
        chunk = buffer = inp.read(4096)
        result = chardet.detect(buffer)
        while chunk and (
            result['confidence'] < 0.9 or result['encoding'] == 'ascii'
        ):
            chunk = inp.read(1024)
            buffer += chunk
            result = chardet.detect(buffer)

        if result['encoding'] == 'ascii':
            # better safe than sorry
            return 'utf-8'
        return result['encoding']


def open_subfile(subfile):
    encoding = detect_file_encoding(subfile)

    with io.open(subfile, encoding=encoding) as reader:
        document = ass.parse(reader)
        newline = next(reversed(sorted(reader.newlines or [], key=len)), None)
        return (document, encoding, newline)


def get_backup_path(pth, key):

    count = 0
    (base, ext) = os.path.splitext(pth)
    newpth = None
    tstamp = time.strftime('%Y%m%d%H%M%S', time.localtime())
    while newpth is None or os.path.exists(newpth):
        newpth = '.'.join([base, key, tstamp, '%03d' % count]) + ext
        count += 1
    return newpth


def update_subfile(
    subfile, subdoc, encoding='utf-8-sig', newline=None, make_backup=True
):

    backup_path = get_backup_path(subfile, 'smartass_backup')
    shutil.copy2(subfile, backup_path)

    try:
        with AtomicWriter(
            subfile, mode='a+', encoding=encoding, newline=newline
        ) as newdata:
            newdata.seek(0)
            newdata.truncate()
            subdoc.dump_file(newdata)
    except Exception:
        shutil.move(backup_path, subfile)
        raise
    if not make_backup and os.path.exists(backup_path):
        os.unlink(backup_path)

    if make_backup:
        LOGGER.debug("updated '%s' (backup: '%s')", subfile, backup_path)
    else:
        LOGGER.debug("updated '%s'", subfile)

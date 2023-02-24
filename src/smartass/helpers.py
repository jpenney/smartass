import re
from abc import ABCMeta, abstractmethod
from html import unescape

from smartypants import Attr, smartypants

__all__ = ['smarten_subtitle_text', 'dumben_subtitle_text']

_NORMALIZE_LEN_CHR = '\u180E'


class Helper(metaclass=ABCMeta):

    _PARTITION_RE = re.compile(
        r'^(?P<prefix>(\{[^\}]*\})+)?'
        r'(?P<body>.*)'
        r'(?P<suffix>(\{[^\}]*\})+)?$'
    )

    _SEGMENT_RE = re.compile(r'((\{[^\}]*\})+|\\[nNh])')

    _TO_DUMB = {
        '\u201c': '"',
        '\u201d': '"',
        '\u2014': '--',
        '\u2026': '...',
        '\u2018': "'",
        '\u2019': "'",
    }

    _DUMB_MAPPING = str.maketrans(_TO_DUMB)

    _NORMALIZE_LEN_MAPPING = str.maketrans(
        dict(
            (k, k.ljust(len(v), _NORMALIZE_LEN_CHR))
            for (k, v) in _TO_DUMB.items()
            if len(k) < len(v)
        )
    )

    def __call__(self, txt):
        return self._execute(txt)

    @abstractmethod
    def _execute(self, txt):
        pass

    def _partition(self, line):
        match = self._PARTITION_RE.match(line)
        if match:
            return tuple(
                (match.group(g) or '') for g in ('prefix', 'body', 'suffix')
            )

        return ('', line, '')

    def _normalize_len(self, txt):
        if _NORMALIZE_LEN_CHR in txt:
            raise RuntimeError(
                'Unable to normalize len because input contains %r'
                % _NORMALIZE_LEN_CHR
            )
        before = txt
        after = txt.translate(self._NORMALIZE_LEN_MAPPING)
        return after

    def _restore_len(self, txt):
        return txt.replace(_NORMALIZE_LEN_CHR, '')

    def _segment(self, txt):

        txt = txt.translate(self._DUMB_MAPPING)
        tags = list(self._SEGMENT_RE.finditer(txt))
        clean = ''

        start = end = i = 0
        for tag in tags:
            start = tag.start()
            end = tag.end()
            if i < start:
                clean += txt[i:start]
            i = end
            # # for \h, \n, \N inject a space in it's place
            if txt[start] == '\\':
                # avoid ".\N.\N." => ". . ." => "…"
                if txt[start - 1] == '.' and txt[end] in ('.', ' '):
                    clean += '-'
                else:
                    clean += ' '

        clean += txt[end:]
        return (clean, tags)

    def _reconstruct(self, clean, tags):
        reconst = ''
        start = end = clean_i = i = 0
        for tag in tags:
            start = tag.start()
            end = tag.end()

            while i < start:
                reconst += clean[clean_i]
                clean_i += 1
                i += 1

            if start <= i:
                addstr = tag.group()
                if addstr.startswith('\\'):
                    # for \h, \n, \N swallow injected space
                    clean_i += 1
                reconst += addstr
                i += len(addstr)

        reconst += clean[clean_i:]
        return reconst

    def _smarten(self, line):  # pylint: disable=R0201
        (body, tags) = self._segment(line)
        return self._restore_len(
            self._reconstruct(
                self._normalize_len(unescape(smartypants(body, Attr.set1))),
                tags,
            )
        )

    def _dumben(self, line):
        (body, tags) = self._segment(line)
        return self._reconstruct(body, tags)


class SmartenHelper(Helper):
    def _execute(self, txt):
        return self._smarten(self._dumben(txt))


class DumbenHelper(Helper):
    def _execute(self, txt):
        return self._dumben(txt)


def smarten_subtitle_text(txt):
    return SmartenHelper()(txt)


def dumben_subtitle_text(txt):
    return DumbenHelper()(txt)

import logging

import click

from . import LOGGER as TOP_LOGGER

LOGGER = logging.getLogger(__name__)

# pylint: disable=R0903


class ClickStream():

    def __init__(self, err=True):
        self._err = err

    def write(self, string):
        click.echo(string, err=self._err, nl=False)


class ClickFormatter(logging.Formatter):

    STYLES = {
        'error': dict(fg='red'),
        'exception': dict(fg='magenta'),
        'critical': dict(fg='magenta', bold=True),
        'debug': dict(dim=True, fg='blue'),
        'warning': dict(fg='yellow')
    }

    _LEVEL_NAME_FMT = '%%%ds' % max(
        len(logging.getLevelName(i)) for i in range(0, 60, 10))

    def __init__(  # pylint: disable=R0913
            self, fmt=None, datefmt=None, style='%',
            show_level_threshold=logging.ERROR,
            show_level_fmt=None, **kwargs):
        self._show_level_threshhold = show_level_threshold
        super().__init__(fmt, datefmt, style, **kwargs)  # noqa
        self._show_level_style = self._default_style = self._style
        if show_level_fmt:
            self._show_level_style = type(self._style)(show_level_fmt)
            if kwargs.get('validate', False) and hasattr(
                    self._show_level_style, 'validate'):
                self._show_level_style.validate()

    def formatMessage(self, record):
        base_style = self.STYLES.get(record.levelname.lower(), {})
        level_style = dict(**base_style)
        level_style['bold'] = True
        new_record = logging.makeLogRecord(record.__dict__)
        new_record.levelname = click.style(
            self._LEVEL_NAME_FMT % new_record.levelname.upper(), **level_style)
        new_record.message = click.style(
            new_record.message, **base_style)

        active_style = self._default_style
        if record.levelno >= self._show_level_threshhold:
            active_style = self._show_level_style

        (self._style, self._fmt) = (active_style,
                                    getattr(active_style, '_fmt', None))
        return click.unstyle(
            '') + super().formatMessage(new_record) + click.unstyle('')


class ClickContextObj():

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._log_level = logging.WARNING
        self._log_handler = None

    def _config_handler(self):
        fmt_args = dict(
            fmt="%(message)s",
            show_level_fmt="%(levelname)s: %(message)s",
            show_level_threshold=logging.ERROR)

        if self.log_level <= logging.DEBUG:
            fmt_args['show_level_threshold'] = self.log_level

        if self.log_level == logging.DEBUG:
            fmt_args['fmt'] += ' (%(name)s)'
            fmt_args['show_level_fmt'] += ' (%(name)s)'

        if self._log_handler:
            logging.root.removeHandler(self._log_handler)
        self._log_handler = logging.StreamHandler(ClickStream(err=False))

        self._log_handler.formatter = ClickFormatter(**fmt_args)

        logging.root.addHandler(self._log_handler)

    @property
    def log_level(self):
        return self._log_level

    @log_level.setter
    def log_level(self, value):
        # logging.root.setLevel(value)
        TOP_LOGGER.setLevel(value)
        self._log_level = value
        self._config_handler()

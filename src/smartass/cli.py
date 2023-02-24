"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will
  cause problems: the code will get executed twice:

  - When you run `python -msmartass` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``smartass.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``smartass.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import logging
from functools import wraps

import click
import pkg_resources

from . import DumbProcessor, SmartProcessor
from .clickutils import ClickContextObj
from .fileutils import open_subfile, update_subfile

LOGGER = logging.getLogger(__name__)


def _common_cli(func):
    default_log_level = logging.getLevelName(logging.INFO).lower()

    @click.option(
        '--log-level',
        type=click.Choice(
            [
                logging.getLevelName(lev).lower()
                for lev in [
                    logging.DEBUG,
                    logging.INFO,
                    logging.WARNING,
                    logging.ERROR,
                    logging.CRITICAL,
                ]
            ]
        ),
        default=default_log_level,
        show_default=True,
        show_choices=True,
        help='log level displayed',
    )
    @click.option(
        '--backup/--no-backup',
        default=True,
        show_default=True,
        help='enable/disable creation of backup files',
    )
    @click.option(
        '--process-comments/--no-process-comments',
        default=False,
        show_default=True,
        help='enable/disable processing of comment events',
    )
    @click.option(
        '--skip-name',
        multiple=True,
        default=[],
        metavar='ACTOR_NAME',
        help=(
            'lines by this actor (case insensitive, uses filename globbing) '
            'will be skipped. May be passed multiple times.'
        ),
    )
    @click.option(
        '--skip-style',
        multiple=True,
        default=[],
        metavar='STYLE_NAME',
        help=(
            'lines in this style (case insensitive, uses filename globbing) '
            'will be skipped. May be passed multiple times.'
        ),
    )
    @click.version_option(
        pkg_resources.get_distribution(__name__.split('.')[0]).version
    )
    @click.argument(
        'subfiles',
        nargs=-1,
        required=True,
        metavar='FILE',
        type=click.Path(
            exists=True, file_okay=True, dir_okay=False, writable=True
        ),
    )
    @click.pass_context
    @wraps(func)
    def wrapper(ctx, log_level, *args, **kwargs):
        obj = ctx.obj = ctx.obj or ClickContextObj()
        level = getattr(logging, log_level.upper())
        obj.log_level = level
        return ctx.invoke(func, *args, **kwargs)

    return wrapper


def _run_cli(
    processor_factory,
    backup,
    process_comments,
    skip_name,
    skip_style,
    subfiles,
):

    processor_args = dict(
        process_comments=process_comments,
        names_to_skip=skip_name,
        styles_to_skip=skip_style,
    )
    processor = processor_factory(**processor_args)

    for subfile in subfiles:
        try:
            (subdoc, encoding, newline) = open_subfile(subfile)

            (
                total_events,
                events_processed,
                events_updated,
            ) = processor.process_document(subdoc, subfile)
            LOGGER.info(
                '%s: events=%d, processed=%d, updated=%d',
                subfile,
                total_events,
                events_processed,
                events_updated,
            )
            if events_updated:
                update_subfile(subfile, subdoc, encoding, newline, backup)
        except RuntimeError as err:
            LOGGER.error('%s: %s: %s', subfile, type(err).__name__, str(err))


@click.command(no_args_is_help=True)
@_common_cli
def smartass(*args, **kwargs):
    """Smarten punctionation on ass subtitle files."""
    _run_cli(SmartProcessor, *args, **kwargs)


@click.command(no_args_is_help=True)
@_common_cli
def dumbass(*args, **kwargs):
    """Unsmarten punctuation on ass subtitle files."""
    _run_cli(DumbProcessor, *args, **kwargs)

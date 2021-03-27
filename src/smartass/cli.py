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
import sys

import click

from . import DumbProcessor, SmartProcessor
from .fileutils import open_subfile, update_subfile


@click.command()
@click.option("--backup/--no-backup", default=True)
@click.option("--process-comments/--no-process-comments", default=False)
@click.option("--skip-name", multiple=True, default=[])
@click.argument('subfiles', nargs=-1)
def main(backup, process_comments, skip_name, subfiles):

    processor_args = dict(
        process_comments=process_comments,
        names_to_skip=skip_name)
    cmd_name = click.get_current_context().info_name
    if cmd_name == 'dumbass':
        processor = DumbProcessor(**processor_args)
    elif cmd_name == 'smartass':
        processor = SmartProcessor(**processor_args)
    else:
        click.echo("Unknown command '%s'" % cmd_name)
        sys.exit(1)
    for subfile in subfiles:
        try:
            (subdoc, encoding, newline) = open_subfile(subfile)

            (total_events, events_processed,
             events_updated) = processor.process_document(subdoc)
            click.echo('%s: events=%d, processed=%d, updated=%d' %
                       (subfile, total_events, events_processed,
                        events_updated))
            if events_updated:
                update_subfile(subfile, subdoc, encoding, newline, backup)
        except RuntimeError as err:
            click.echo(
                "ERROR: %s: %s: %s" %
                (subfile, type(err).__name__, str(err)))

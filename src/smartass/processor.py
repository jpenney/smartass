import logging
import re
from abc import ABCMeta, abstractmethod
from fnmatch import fnmatch

from ass import Comment, Dialogue, Document

from .helpers import dumben_subtitle_text, smarten_subtitle_text

LOGGER = logging.getLogger(__name__)

__all__ = ['SmartProcessor', 'DumbProcessor']


class Processor(metaclass=ABCMeta):
    def __init__(
        self,
        make_backups=True,
        process_comments=False,
        names_to_skip=None,
        styles_to_skip=None,
    ):
        self._make_backups = make_backups

        supported_events = set([Dialogue])
        if process_comments:
            supported_events.add(Comment)

        self._supported_events = tuple(e for e in supported_events)
        self._names_to_skip = set([])
        self._styles_to_skip = set([])
        self._current_subfile = None

        if names_to_skip:
            self._names_to_skip = set(names_to_skip)
        if styles_to_skip:
            self._styles_to_skip = set(styles_to_skip)

    @property
    def current_subfile(self):
        return self._current_subfile

    @property
    def make_backups(self):
        return self._make_backups

    def _smarten(self, line):  # pylint: disable=R0201
        return smarten_subtitle_text(line)

    def _dumben(self, line):
        return dumben_subtitle_text(line)

    @abstractmethod
    def _process_text(self, line):
        pass

    def event_supported(self, event):
        if not isinstance(event, self._supported_events):
            return False

        if event.name:
            for skip_pattern in self._names_to_skip:
                LOGGER.info('comparing %s <=> %s', event.name, skip_pattern)
                if fnmatch(event.name, skip_pattern):
                    return False

        if event.style:
            for skip_pattern in self._styles_to_skip:
                LOGGER.info('comparing %s <=> %s', event.style, skip_pattern)
                if fnmatch(event.style, skip_pattern):
                    return False

        return True

    def _process_event(self, event):
        if not self.event_supported(event):
            return False
        new_text = self._process_text(event.text)
        if new_text == event.text:
            return False
        event.text = new_text
        return True

    def process_document(self, document, subfile=None):
        if not isinstance(document, Document):
            raise TypeError("'document' (%r) unsupported")
        total_events = 0
        events_processed = 0
        events_updated = 0
        self._current_subfile = subfile
        try:
            for event in document.events:
                total_events += 1
                if self.event_supported(event):
                    events_processed += 1
                    if self._process_event(event):
                        events_updated += 1
        finally:
            self._current_subfile = None

        return (total_events, events_processed, events_updated)

    def process_text(self, text):
        return self._process_text(text)


class SmartProcessor(Processor):
    def _process_text(self, line):
        return self._smarten(self._dumben(line))


class DumbProcessor(Processor):
    def _process_text(self, line):
        return self._dumben(line)

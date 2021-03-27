from abc import ABCMeta, abstractmethod
from html import unescape

from ass import Comment, Dialogue, Document
from smartypants import smartypants

__all__ = ['SmartProcessor', 'DumbProcessor']


class Processor(metaclass=ABCMeta):

    _DUMB_MAPPING = str.maketrans({
        '\u201c': '"',
        '\u201d': '"',
        '\u2014': '--',
        '\u2026': '...',
        '\u2018': "'",
        '\u2019': "'"})

    def __init__(
            self, make_backups=True, process_comments=False,
            names_to_skip=None):
        self._make_backups = make_backups

        supported_events = set([Dialogue])
        if process_comments:
            supported_events.add(Comment)

        self._supported_events = tuple(e for e in supported_events)
        self._names_to_skip = set([])
        if names_to_skip:
            self._names_to_skip = set(n.lower() for n in names_to_skip)

    @property
    def make_backups(self):
        return self._make_backups

    def _smarten(self, line):  # pylint: disable=R0201
        return unescape(smartypants(line))

    def _dumben(self, line):
        return line.translate(self._DUMB_MAPPING)

    @abstractmethod
    def _process_text(self, line):
        pass

    def event_supported(self, event):
        if not isinstance(event, self._supported_events):
            return False

        if (event.name and self._names_to_skip and
                event.name.lower() in self._names_to_skip):
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

    def process_document(self, document):
        if not isinstance(document, Document):
            raise TypeError("'document' (%r) unsupported")
        total_events = 0
        events_processed = 0
        events_updated = 0

        for event in document.events:
            total_events += 1
            if self.event_supported(event):
                events_processed += 1
                if self._process_event(event):
                    events_updated += 1

        return (total_events, events_processed, events_updated)


class SmartProcessor(Processor):

    def _process_text(self, line):
        return self._smarten(self._dumben(line))


class DumbProcessor(Processor):

    def _process_text(self, line):
        return self._dumben(line)

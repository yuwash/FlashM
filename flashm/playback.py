from collections import deque
from itertools import islice
import math
import random


class Deck(object):
    def __init__(self, initial_keys=None):
        self.data = []
        self.data_ordered = []
        if initial_keys is None:
            self.count = 0
        else:
            self.data.append(set(initial_keys))
            self.data_ordered.append(deque(initial_keys))
            self.count = len(initial_keys)
            if not self.count == len(self.data[0]):
                raise ValueError('initial_keys contains duplicates!')

    def __repr__(self):
        return 'Deck([{}])'.format(', '.join(
            '[{}]'.format(', '.join(repr(key) for key in level_data))
            # avoid printing "deque([..])" for every level_data
            for level_data in self.data_ordered))

    def get_current_level(self, key):
        for level in range(len(self.data)):
            if key in self.data[level]:
                return level
        return -1

    def up(self, key):
        """
        >>> deck = Deck()
        >>> for key in 'abcda':
        ...     deck.up(key)
        >>> deck
        Deck([['b', 'c', 'd'], ['a']])
        >>> for key in 'daa':
        ...     deck.up(key)
        >>> deck
        Deck([['b', 'c'], ['d'], [], ['a']])
        """
        current_level = self.get_current_level(key)
        if current_level == -1:
            self.count += 1
        else:
            self.data[current_level].remove(key)
            self.data_ordered[current_level].remove(key)
        if len(self.data) == current_level + 1:
            self.data.append(set())
            self.data_ordered.append(deque())
        self.data[current_level + 1].add(key)
        self.data_ordered[current_level + 1].append(key)

    def get_at_rank(self, rank):
        level_rank = rank
        if rank < 0:
            for level_data in reversed(self.data_ordered):
                level_rank += len(level_data)
                if 0 <= level_rank:
                    return level_data[level_rank]
        else:
            for level_data in self.data_ordered:
                level_rank -= len(level_data)
                if level_rank < 0:
                    return level_data[level_rank]
        raise ValueError('rank out of range')


def playback_from_deck(deck):
    """
    >>> deck = Deck(initial_keys='abcd')
    >>> deck.up('d')
    >>> from unittest.mock import patch
    >>> with patch.object(
    ...         random, 'expovariate', side_effect=(1e-9, 0.1, 0.5, 1, 2)):
    ...     for key in playback_from_deck(deck):
    ...         print(key)
    c
    d
    b
    a
    c
    """
    if 1 < deck.count:
        while True:
            max_rank = deck.count - 1  # avoid the very last reviewed
            rank = -2 - min(
                max_rank - 1,
                int(max_rank*random.expovariate(1/math.log(2))))
            key = deck.get_at_rank(rank)
            deck.up(key)
            yield key
    elif 1 == deck.count:
        key = deck.get_at_rank(0)
        deck.up(key)
        yield key
    # nothing to yield if empty


def playback_iter(items, unit=2, reps=2):
    """
    >>> list(playback_iter('abcde', unit=3))
    ['a', 'b', 'c', 'a', 'b', 'c', 'd', 'e', None, 'd', 'e', None]
    """
    len_in_unit, remaining = divmod(len(items), unit)
    for unit_start in range(0, unit*len_in_unit, unit):
        unit_stop = unit_start + unit
        for _ in range(reps):
            for item in islice(items, unit_start, unit_stop):
                yield item
    for _ in range(reps):
        for item in islice(items, unit*len_in_unit, None):
            yield item
        if remaining:
            for _ in range(unit - remaining):
                yield  # fill up to the next full unit with None


def playback_into_deck(deck, items, unit=2, reps=2):
    """
    >>> deck = Deck(initial_keys='a')
    >>> from unittest.mock import patch
    >>> with patch.object(
    ...         random, 'expovariate', return_value=1):
    ...     print(''.join(playback_into_deck(deck, 'bc')))
    bcabca
    >>> deck
    Deck([[], ['b', 'c'], ['a']])
    """
    for i, key in enumerate(playback_iter(items, unit=unit, reps=reps)):
        review_size = int(deck.count**0.5) if i % unit == unit - 1 else 0
        if key is not None:
            deck.up(key)
            yield key
        elif review_size < 1:
            review_size = 1
        for key in islice(playback_from_deck(deck), review_size):
            yield key  # deck.up already called

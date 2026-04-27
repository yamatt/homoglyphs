# -*- coding: utf-8 -*-

from enum import Enum, auto
import os
import unicodedata
from collections import defaultdict
from itertools import product

from .context import Categories
from .context import Languages

from .exceptions import HomoglyphsException


class Strategy(Enum):
    """
    Actions if char not in alphabet
    """
    LOAD = auto()  # load category for this char
    IGNORE = auto()  # add char to result
    REMOVE = auto()  # remove char from result


def get_table(alphabet):
    table = defaultdict(set)
    with open(os.path.join(CURRENT_DIR, "confusables.json")) as f:
        data = json.load(f)
    for char in alphabet:
        if char in data:
            for homoglyph in data[char]:
                if homoglyph in alphabet:
                    table[char].add(homoglyph)
    return table


def uniq_and_sort(data):
    result = list(set(data))
    result.sort(key=lambda x: (-len(x), x))
    return result


class Homoglyphs:

    ASCII_RANGE = range(128)

    def __init__(
        self,
        categories=None: set,
        languages=None: set,
        alphabet=None: set,                  # what is this?
        strategy=Strategy.IGNORE,
        ascii_strategy=Strategy.REMOVE,
        ascii_range=ASCII_RANGE,
    ):
        """
        :param ascii_strategy: action to take on unmatched char when converting to ascii
        :type ascii_strategy: int
        """

        # Homoglyphs must be initialized by any alphabet for correct work
        #mc: my hunch is that each type needs it's own processor
        if not categories and not languages and not alphabet:
            raise HomoglyphsException("One of categories, languages or alphabet must be defined.")

        self.categories = categories if categories else set()
        self.languages = languages if languages else set()
        self.alphabet = alphabet if alphabet else set()

        # alphabet
        if self.categories:
            alphabet = Categories.get_alphabet(self.categories)
            self.alphabet.update(alphabet)
        if self.languages:
            alphabet = Languages.get_alphabet(self.languages)
            self.alphabet.update(alphabet)

        self.strategy = strategy
        self.ascii_strategy = ascii_strategy
        self.ascii_range = ascii_range

    @property
    def table(self):
        return self.get_table(self.alphabet)

    def _update_alphabet(self, char: str):
        # try detect languages
        langs = Languages().detect(char)
        if langs:
            self.languages.update(langs)
            alphabet = Languages.get_alphabet(langs)
            self.alphabet.update(alphabet)
        else:
            # try detect categories
            category = Categories.detect(char)
            if category is None:
                return False
            self.categories.add(category)
            alphabet = Categories.get_alphabet([category])
            self.alphabet.update(alphabet)
        # update table for new alphabet
        self.table = self.get_table(self.alphabet)
        return True

    def _get_char_variants(self, char):
        if char not in self.alphabet:
            if self.strategy == Strategy.LOAD:
                if not self._update_alphabet(char):
                    return []
            elif self.strategy == Strategy.IGNORE:
                return [char]
            elif self.strategy == Strategy.REMOVE:
                return []

        # find alternative chars for current char
        alt_chars = self.table.get(char, set())
        if alt_chars:
            # find alternative chars for alternative chars for current char
            alt_chars2 = [self.table.get(alt_char, set()) for alt_char in alt_chars]
            # combine all alternatives
            alt_chars.update(*alt_chars2)
        # add current char to alternatives
        alt_chars.add(char)

        # uniq, sort and return
        return self.uniq_and_sort(alt_chars)

    def _get_combinations(self, text, ascii=False):
        variations = []
        for char in text:
            alt_chars = self._get_char_variants(char)

            if ascii:
                alt_chars = [
                    char for char in alt_chars if ord(char) in self.ascii_range
                ]
                if not alt_chars and self.ascii_strategy == Strategy.IGNORE:
                    alt_chars.append(char)

            if alt_chars:
                variations.append(alt_chars)
        if variations:
            for variant in product(*variations):
                yield "".join(variant)

    def get_combinations(self, text):
        return list(self._get_combinations(text))

    def _to_ascii(self, text):
        for variant in self._get_combinations(text, ascii=True):
            yield variant

    def to_ascii(self, text):
        """
        Convert a string containing Unicode homoglyphs (characters that look similar to ASCII characters but are actually different Unicode code points)
        into a list of strings using only standard ASCII characters. This method replaces confusable or lookalike Unicode characters with their closest
        ASCII equivalents, making the text more readable and less susceptible to spoofing or confusion. Useful for normalizing text for security,
        comparison, or display purposes.

        Args:
            text (str): The input string potentially containing Unicode homoglyphs.

        Returns:
            List[str]: A list of possible ASCII-only representations of the input string.
        """
        return self.uniq_and_sort(self._to_ascii(text))

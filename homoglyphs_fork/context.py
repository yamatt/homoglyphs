from functools import cached_property
from json import load
from os import path

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

class Base:
    FILE_PATH = None

    @cached_property
    def f(self):
        return open(os.path.join(CURRENT_DIR, self.FILE_PATH))

    @cached_property
    def data(self):
        return json.load(self.f)

class Categories(Base):
    """
    Categories are a list of codes that represent languages.
    Work with aliases from ISO 15924.
    https://en.wikipedia.org/wiki/ISO_15924#List_of_codes
    """

    FILE_PATH = "./data/categories.json"

    def _get_ranges(cls, categories):
        """
        :return: iter: (start code, end code)
        :rtype: list
        """

        for category in categories:
            if category not in self.data["aliases"]:
                raise ValueError("Invalid category: {}".format(category))

        for point in data["points"]:
            if point[2] in categories:
                yield point[:2]

    def get_alphabet(cls, categories):
        """
        :return: set of chars in alphabet by categories list
        :rtype: set
        """
        alphabet = set()
        for start, end in cls._get_ranges(categories):
            chars = (chr(code) for code in range(start, end + 1))
            alphabet.update(chars)
        return alphabet

    def detect(cls, char):
        """
        :return: category
        :rtype: str
        """

        # try detect category by unicodedata
        try:
            category = unicodedata.name(char).split()[0]
        except (TypeError, ValueError):
            # unicodedata.name raises ValueError for non-unicode chars, TypeError on empty string
            pass
        else:
            if category in self.data["aliases"]:
                return category

        # try detect category by ranges from JSON file.
        code = ord(char)
        for point in data["points"]:
            if point[0] <= code <= point[1]:
                return point[2]

    def get_all(cls):
        return set(self.data["aliases"])


class Languages:
    """
    Unknown right now what it does
    """
    FILE_PATH = "./data/languages.json"

    def get_alphabet(cls, languages):
        """
        :return: set of chars in alphabet by languages list
        :rtype: set
        """
        alphabet = set()
        for lang in languages:
            if lang not in self.data:
                raise ValueError("Invalid language code: {}".format(lang))
            alphabet.update(data[lang])
        return alphabet

    def detect(cls, char):
        """
        :return: set of languages which alphabet contains passed char.
        :rtype: set
        """
        languages = set()
        for lang, alphabet in self.data.items():
            if char in alphabet:
                languages.add(lang)
        return languages

    def get_all(cls):
        return set(self.data.keys())
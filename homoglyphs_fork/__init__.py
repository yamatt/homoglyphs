"""
Homoglyphs

* Get similar letters
* Convert string to ASCII letters
* Detect possible letter languages
* Detect letter UTF-8 group.
"""

# main package info
__title__ = "Homoglyphs"
__author__ = "Gram Orsinium"
__license__ = "MIT"


from .core import STRATEGY_REMOVE  # noQA
from .core import STRATEGY_IGNORE, STRATEGY_LOAD, Categories, Homoglyphs, Languages

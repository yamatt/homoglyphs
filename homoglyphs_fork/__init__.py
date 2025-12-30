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


from .core import (  # noQA
    Categories,
    Languages,
    Homoglyphs,
    STRATEGY_LOAD,
    STRATEGY_IGNORE,
    STRATEGY_REMOVE,
)

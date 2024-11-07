# -*- coding: utf-8 -*-
import unittest
from homoglyphs_fork import (
    Categories, Languages, Homoglyphs,
    STRATEGY_LOAD, STRATEGY_IGNORE, STRATEGY_REMOVE
)


CIRILLIC_ES = u'с'
CIRILLIC_HE = u'х'


class TestCommon(unittest.TestCase):
    def test_detect_category(self):
        self.assertEqual(Categories.detect('d'), 'LATIN')
        self.assertEqual(Categories.detect(u'Д'), 'CYRILLIC')
        self.assertEqual(Categories.detect('?'), 'COMMON')
        self.assertEqual(Categories.detect(u'ㅡ'), 'HANGUL')

    def test_detect_language(self):
        self.assertIn('en', Languages.detect('d'))
        self.assertIn('ru', Languages.detect(u'Д'))
        self.assertEqual(Languages.detect('?'), set())

    def test_get_alphabet_cat(self):
        alphabet = Categories.get_alphabet(['LATIN'])
        self.assertIn('s', alphabet)
        self.assertIn('S', alphabet)
        self.assertNotIn(u'ё', alphabet)
        self.assertGreater(len(alphabet), 50)
        self.assertLess(len(alphabet), 1400)

        alphabet = Categories.get_alphabet(['CYRILLIC'])
        self.assertIn(u'ё', alphabet)
        self.assertIn(u'Ё', alphabet)
        self.assertNotIn('s', alphabet)
        self.assertGreater(len(alphabet), 50)
        self.assertLess(len(alphabet), 500)

        alphabet = Categories.get_alphabet(['HANGUL'])
        self.assertIn(u'ㅡ', alphabet)

    def test_get_alphabet_lang(self):
        alphabet = Languages.get_alphabet({'en'})
        self.assertIn('s', alphabet)
        self.assertIn('S', alphabet)
        self.assertNotIn(u'ё', alphabet)
        self.assertEqual(len(alphabet), 26 * 2)

        alphabet = Languages.get_alphabet({'ru'})
        self.assertIn(u'ё', alphabet)
        self.assertIn(u'Ё', alphabet)
        self.assertNotIn('s', alphabet)
        self.assertEqual(len(alphabet), 33 * 2)

    def test_get_table(self):
        alphabet = Categories.get_alphabet(['LATIN'])
        table = Homoglyphs.get_table(alphabet)
        self.assertIn('s', table)
        self.assertNotIn(CIRILLIC_ES, table)

        alphabet = Categories.get_alphabet(['HANGUL', 'COMMON'])
        table = Homoglyphs.get_table(alphabet)
        self.assertGreater(len(table[u'ㅡ']), 0)

    def test_get_char_variants(self):
        variants = Homoglyphs(['LATIN'])._get_char_variants('s')
        self.assertIn('s', variants)
        self.assertIn(u'ｓ', variants)
        self.assertNotIn('S', variants)
        self.assertNotIn(CIRILLIC_ES, variants)

        variants = Homoglyphs(['LATIN'])._get_char_variants('c')
        self.assertIn('c', variants)
        self.assertNotIn(CIRILLIC_ES, variants)

        variants = Homoglyphs(['LATIN', 'CYRILLIC'])._get_char_variants('c')
        self.assertIn('c', variants)
        self.assertIn(CIRILLIC_ES, variants)

    def test_strategy(self):
        variants = Homoglyphs(['LATIN'], strategy=STRATEGY_IGNORE)._get_char_variants(u'ё')
        self.assertEqual(variants, [u'ё'])

        variants = Homoglyphs(['LATIN'], strategy=STRATEGY_LOAD)._get_char_variants(CIRILLIC_HE)
        self.assertGreater(len(variants), 1)
        self.assertIn('x', variants)
        self.assertIn(CIRILLIC_HE, variants)

        variants = Homoglyphs(['LATIN'], strategy=STRATEGY_REMOVE)._get_char_variants(CIRILLIC_HE)
        self.assertEqual(variants, [])

        for s in (STRATEGY_REMOVE, STRATEGY_IGNORE, STRATEGY_LOAD):
            variants = Homoglyphs(['LATIN'], strategy=s)._get_char_variants('d')
            self.assertIn('d', variants)

    def test_to_ascii(self):
        ss = Homoglyphs(strategy=STRATEGY_LOAD).to_ascii(CIRILLIC_HE)
        self.assertEqual(ss, ['x'])

        ss = Homoglyphs(strategy=STRATEGY_LOAD).to_ascii(CIRILLIC_HE)
        self.assertEqual(ss, ['x'])

        ss = Homoglyphs(strategy=STRATEGY_LOAD, ascii_range=range(256)).to_ascii(CIRILLIC_HE + u'23.')
        self.assertEqual(ss, ['x23.', u'×23.'])

        homoglyphs = Homoglyphs(languages={'en'}, strategy=STRATEGY_LOAD)
        self.assertEqual(homoglyphs.to_ascii('ТЕСТ'), ['TECT'])

    def test_ascii_strategy(self):
        ss = Homoglyphs(
            categories=('LATIN', 'COMMON', 'CYRILLIC'),
            ascii_strategy=STRATEGY_IGNORE,
        ).to_ascii(u'xхч2')
        self.assertEqual(ss, [u'xxч2'])

        ss = Homoglyphs(
            categories=('LATIN', 'COMMON', 'CYRILLIC'),
            ascii_strategy=STRATEGY_REMOVE,
            ascii_range=range(256),
        ).to_ascii(u'xхч2')
        self.assertEqual(ss, ['xx2', u'x×2', u'×x2', u'××2'])

        ss = Homoglyphs(
            strategy=STRATEGY_LOAD,
            ascii_strategy=STRATEGY_REMOVE,
        ).to_ascii(u'ч')
        self.assertEqual(ss, [])

        # this test is based on https://github.com/yamatt/homoglyphs/issues/4
        ss = Homoglyphs(ascii_strategy=STRATEGY_IGNORE).to_ascii('ß')
        self.assertEqual(ss, ['ß'])


        # # This char hasn't been added yet :/
        # ss = Homoglyphs(
        #     strategy=STRATEGY_LOAD,
        #     ascii_strategy=STRATEGY_REMOVE,
        # ).to_ascii(u'ㅡ')
        # self.assertEqual(ss, ['-'])


if __name__ == '__main__':
    unittest.main()

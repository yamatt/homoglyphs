# -*- coding: utf-8 -*-
import unittest
from homoglyphs import Homoglyphs, STRATEGY_LOAD, STRATEGY_IGNORE, STRATEGY_REMOVE


CIRILLIC_ES = u'с'
CIRILLIC_HE = u'х'


class TestCommon(unittest.TestCase):
    def test_detect_category(self):
        self.assertEqual(Homoglyphs.detect_category('d'), 'LATIN')
        self.assertEqual(Homoglyphs.detect_category(u'Д'), 'CYRILLIC')
        self.assertEqual(Homoglyphs.detect_category('?'), 'COMMON')

    def test_get_alphabet(self):
        alphabet = Homoglyphs.get_alphabet(['LATIN'])
        self.assertIn('s', alphabet)
        self.assertIn('S', alphabet)
        self.assertNotIn(u'ё', alphabet)
        self.assertGreater(len(alphabet), 50)
        self.assertLess(len(alphabet), 1400)

        alphabet = Homoglyphs.get_alphabet(['CYRILLIC'])
        self.assertIn(u'ё', alphabet)
        self.assertIn(u'Ё', alphabet)
        self.assertNotIn('s', alphabet)
        self.assertGreater(len(alphabet), 50)
        self.assertLess(len(alphabet), 500)

    def test_get_table(self):
        alphabet = Homoglyphs.get_alphabet(['LATIN'])
        table = Homoglyphs.get_table(alphabet)
        self.assertIn('s', table)
        self.assertNotIn(CIRILLIC_ES, table)

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

        ss = Homoglyphs(strategy=STRATEGY_LOAD).to_ascii(CIRILLIC_HE + u'23.')
        self.assertEqual(ss, ['x23.'])

        ss = Homoglyphs(
            categories=('LATIN', 'COMMON', 'CYRILLIC'),
            ascii_strategy=STRATEGY_REMOVE,
        ).to_ascii(u'xхч2')
        self.assertEqual(ss, ['xx2'])


if __name__ == '__main__':
    unittest.main()
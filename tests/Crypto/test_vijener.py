import unittest
from src.Crypto import Vijener


class TestVijener(unittest.TestCase):

    def setUp(self):
        self.vijener_without_key = Vijener()
        self.vijener_with_key_eng = Vijener('Pkgap')
        self.vijener_with_key_rus = Vijener('Юижры')

    def test_get_new_char_without_key_eng_encode(self):
        self.vijener_without_key.check_key("Hello")
        self.assertEqual(self.vijener_without_key.get_new_char('H', Vijener.ENCODE), 'A')
        self.assertEqual(self.vijener_without_key.get_new_char('e', Vijener.ENCODE), 'l')
        self.assertEqual(self.vijener_without_key.get_new_char('l', Vijener.ENCODE), 'p')
        self.assertEqual(self.vijener_without_key.get_new_char('l', Vijener.ENCODE), 'q')
        self.assertEqual(self.vijener_without_key.get_new_char('o', Vijener.ENCODE), 'w')

    def test_get_new_char_with_key_eng_encode(self):
        self.assertEqual(self.vijener_with_key_eng.get_new_char('H', Vijener.ENCODE), 'W')
        self.assertEqual(self.vijener_with_key_eng.get_new_char('e', Vijener.ENCODE), 'o')
        self.assertEqual(self.vijener_with_key_eng.get_new_char('l', Vijener.ENCODE), 'r')
        self.assertEqual(self.vijener_with_key_eng.get_new_char('l', Vijener.ENCODE), 'l')
        self.assertEqual(self.vijener_with_key_eng.get_new_char('o', Vijener.ENCODE), 'd')

    def test_get_new_char_without_key_eng_decode(self):
        self.vijener_without_key.check_key("Alpqw")
        self.assertEqual(self.vijener_without_key.get_new_char('A', Vijener.DECODE), 'H')
        self.assertEqual(self.vijener_without_key.get_new_char('l', Vijener.DECODE), 'e')
        self.assertEqual(self.vijener_without_key.get_new_char('p', Vijener.DECODE), 'l')
        self.assertEqual(self.vijener_without_key.get_new_char('q', Vijener.DECODE), 'l')
        self.assertEqual(self.vijener_without_key.get_new_char('w', Vijener.DECODE), 'o')

    def test_get_new_char_with_key_eng_decode(self):
        self.assertEqual(self.vijener_with_key_eng.get_new_char('W', Vijener.DECODE), 'H')
        self.assertEqual(self.vijener_with_key_eng.get_new_char('o', Vijener.DECODE), 'e')
        self.assertEqual(self.vijener_with_key_eng.get_new_char('r', Vijener.DECODE), 'l')
        self.assertEqual(self.vijener_with_key_eng.get_new_char('l', Vijener.DECODE), 'l')
        self.assertEqual(self.vijener_with_key_eng.get_new_char('d', Vijener.DECODE), 'o')

    def test_get_new_char_without_key_rus_encode(self):
        self.vijener_without_key.check_key("Салют")
        self.assertEqual(self.vijener_without_key.get_new_char('С', Vijener.ENCODE), 'Й')
        self.assertEqual(self.vijener_without_key.get_new_char('а', Vijener.ENCODE), 'е')
        self.assertEqual(self.vijener_without_key.get_new_char('л', Vijener.ENCODE), 'а')
        self.assertEqual(self.vijener_without_key.get_new_char('ю', Vijener.ENCODE), 'а')
        self.assertEqual(self.vijener_without_key.get_new_char('т', Vijener.ENCODE), 'ъ')

    def test_get_new_char_with_key_rus_encode(self):
        self.assertEqual(self.vijener_with_key_rus.get_new_char('С', Vijener.ENCODE), 'П')
        self.assertEqual(self.vijener_with_key_rus.get_new_char('а', Vijener.ENCODE), 'и')
        self.assertEqual(self.vijener_with_key_rus.get_new_char('л', Vijener.ENCODE), 'т')
        self.assertEqual(self.vijener_with_key_rus.get_new_char('ю', Vijener.ENCODE), 'о')
        self.assertEqual(self.vijener_with_key_rus.get_new_char('т', Vijener.ENCODE), 'н')

    def test_get_new_char_without_key_rus_decode(self):
        self.vijener_without_key.check_key("Йуааъ")
        self.assertEqual(self.vijener_without_key.get_new_char('Й', Vijener.DECODE), 'С')
        self.assertEqual(self.vijener_without_key.get_new_char('е', Vijener.DECODE), 'а')
        self.assertEqual(self.vijener_without_key.get_new_char('а', Vijener.DECODE), 'л')
        self.assertEqual(self.vijener_without_key.get_new_char('а', Vijener.DECODE), 'ю')
        self.assertEqual(self.vijener_without_key.get_new_char('ъ', Vijener.DECODE), 'т')

    def test_get_new_char_with_key_rus_decode(self):
        self.assertEqual(self.vijener_with_key_rus.get_new_char('П', Vijener.DECODE), 'С')
        self.assertEqual(self.vijener_with_key_rus.get_new_char('и', Vijener.DECODE), 'а')
        self.assertEqual(self.vijener_with_key_rus.get_new_char('т', Vijener.DECODE), 'л')
        self.assertEqual(self.vijener_with_key_rus.get_new_char('о', Vijener.DECODE), 'ю')
        self.assertEqual(self.vijener_with_key_rus.get_new_char('н', Vijener.DECODE), 'т')

    def test_get_new_char_not_letter_encode(self):
        self.assertEqual(self.vijener_without_key.get_new_char('@@@@', Vijener.ENCODE), '@@@@')
        self.assertEqual(self.vijener_with_key_rus.get_new_char('@@@@', Vijener.ENCODE), '@@@@')
        self.assertEqual(self.vijener_with_key_eng.get_new_char('@@@@', Vijener.ENCODE), '@@@@')

    def test_get_new_char_not_letter_decode(self):
        self.assertEqual(self.vijener_without_key.get_new_char(',!@#', Vijener.DECODE), ',!@#')
        self.assertEqual(self.vijener_with_key_eng.get_new_char(',!@#', Vijener.DECODE), ',!@#')
        self.assertEqual(self.vijener_with_key_rus.get_new_char(',!@#', Vijener.DECODE), ',!@#')

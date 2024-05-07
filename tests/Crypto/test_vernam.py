import unittest
from src.Crypto import Vernam


class TestVernam(unittest.TestCase):

    def setUp(self):
        self.Vernam_without_key = Vernam()
        self.Vernam_with_key_eng = Vernam('Son')
        self.Vernam_with_key_rus = Vernam('Сон')

    def test_get_new_char_without_key_eng_encode(self):
        self.Vernam_without_key.check_key("God")
        self.assertEqual(self.Vernam_without_key.get_new_char('G', Vernam.ENCODE), 'V')
        self.assertEqual(self.Vernam_without_key.get_new_char('o', Vernam.ENCODE), 'j')
        self.assertEqual(self.Vernam_without_key.get_new_char('d', Vernam.ENCODE), 'h')

    def test_get_new_char_with_key_eng_encode(self):
        self.assertEqual(self.Vernam_with_key_eng.get_new_char('G', Vernam.ENCODE), 'U')
        self.assertEqual(self.Vernam_with_key_eng.get_new_char('o', Vernam.ENCODE), 'a')
        self.assertEqual(self.Vernam_with_key_eng.get_new_char('d', Vernam.ENCODE), 'o')

    def test_get_new_char_without_key_eng_decode(self):
        self.Vernam_without_key.check_key("Vjh")
        self.assertEqual(self.Vernam_without_key.get_new_char('V', Vernam.DECODE), 'G')
        self.assertEqual(self.Vernam_without_key.get_new_char('j', Vernam.DECODE), 'o')
        self.assertEqual(self.Vernam_without_key.get_new_char('h', Vernam.DECODE), 'd')

    def test_get_new_char_with_key_eng_decode(self):
        self.assertEqual(self.Vernam_with_key_eng.get_new_char('U', Vernam.DECODE), 'G')
        self.assertEqual(self.Vernam_with_key_eng.get_new_char('a', Vernam.DECODE), 'o')
        self.assertEqual(self.Vernam_with_key_eng.get_new_char('o', Vernam.DECODE), 'd')

    def test_get_new_char_without_key_rus_encode(self):
        self.Vernam_without_key.check_key("Гол")
        self.assertEqual(self.Vernam_without_key.get_new_char('Г', Vernam.ENCODE), 'Ы')
        self.assertEqual(self.Vernam_without_key.get_new_char('о', Vernam.ENCODE), 'л')
        self.assertEqual(self.Vernam_without_key.get_new_char('л', Vernam.ENCODE), 'я')

    def test_get_new_char_with_key_rus_encode(self):
        self.assertEqual(self.Vernam_with_key_rus.get_new_char('Г', Vernam.ENCODE), 'Т')
        self.assertEqual(self.Vernam_with_key_rus.get_new_char('о', Vernam.ENCODE), 'а')
        self.assertEqual(self.Vernam_with_key_rus.get_new_char('л', Vernam.ENCODE), 'ж')

    def test_get_new_char_without_key_rus_decode(self):
        self.Vernam_without_key.check_key("Ыля")
        self.assertEqual(self.Vernam_without_key.get_new_char('Ы', Vernam.DECODE), 'Г')
        self.assertEqual(self.Vernam_without_key.get_new_char('л', Vernam.DECODE), 'о')
        self.assertEqual(self.Vernam_without_key.get_new_char('я', Vernam.DECODE), 'л')

    def test_get_new_char_with_key_rus_decode(self):
        self.assertEqual(self.Vernam_with_key_rus.get_new_char('Т', Vernam.DECODE), 'Г')
        self.assertEqual(self.Vernam_with_key_rus.get_new_char('а', Vernam.DECODE), 'о')
        self.assertEqual(self.Vernam_with_key_rus.get_new_char('ж', Vernam.DECODE), 'л')

    def test_get_new_char_not_letter_encode(self):
        self.assertEqual(self.Vernam_without_key.get_new_char('@@@', Vernam.ENCODE), '@@@')
        self.assertEqual(self.Vernam_with_key_rus.get_new_char('@@@', Vernam.ENCODE), '@@@')
        self.assertEqual(self.Vernam_with_key_eng.get_new_char('@@@', Vernam.ENCODE), '@@@')

    def test_get_new_char_not_letter_decode(self):
        self.assertEqual(self.Vernam_without_key.get_new_char('!@#', Vernam.DECODE), '!@#')
        self.assertEqual(self.Vernam_with_key_eng.get_new_char('!@#', Vernam.DECODE), '!@#')
        self.assertEqual(self.Vernam_with_key_rus.get_new_char('!@#', Vernam.DECODE), '!@#')

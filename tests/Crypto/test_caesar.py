import unittest
from src.Crypto import Caesar


class TestCaesar(unittest.TestCase):

    def test_init_without_key(self):
        self.assertEqual(Caesar().key, 3)

    def test_init_with_key(self):
        self.assertEqual(Caesar(5).key, 5)

    def test_get_new_char_eng_encode(self):
        self.assertEqual(Caesar(1).get_new_char('Z', Caesar.ENCODE), 'A')

    def test_get_new_char_eng_decode(self):
        self.assertEqual(Caesar(2).get_new_char('d', Caesar.DECODE), 'b')

    def test_get_new_char_rus_encode(self):
        self.assertEqual(Caesar(1).get_new_char('Я', Caesar.ENCODE), 'А')

    def test_get_new_char_rus_decode(self):
        self.assertEqual(Caesar(2).get_new_char('ж', Caesar.DECODE), 'е')

    def test_get_new_char_not_letter_encode(self):
        self.assertEqual(Caesar(1).get_new_char('@', Caesar.ENCODE), '@')

    def test_get_new_char_not_letter_decode(self):
        self.assertEqual(Caesar(2).get_new_char(',', Caesar.DECODE), ',')

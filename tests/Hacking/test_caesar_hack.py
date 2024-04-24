import os
import unittest
from src.Hacking import CaesarHack


class TestCaesarHack(unittest.TestCase):

    def test_set_language_index_rus(self):
        hacker = CaesarHack()
        hacker.set_language_index('Привет')
        self.assertEqual(hacker.alphabet_index, 0)

    def test_set_language_index_eng(self):
        hacker = CaesarHack()
        hacker.set_language_index('Hello')
        self.assertEqual(hacker.alphabet_index, 1)

    def test_caesar_hacker_no_letters(self):
        hacker = CaesarHack()
        filename = 'test000.txt'
        with open(filename, 'w') as f:
            f.write('12233')
        result = hacker.caesar_hacker(filename)
        self.assertIsNone(result)
        os.remove(filename)

    def test_caesar_hacker_eng_text(self):
        hacker = CaesarHack()
        filename = 'test000.txt'
        with open(filename, 'w') as f:
            f.write('Xnc ujtuqj bjwj pnqqji fsi')
        result_filename = hacker.caesar_hacker(filename)
        with open(result_filename, 'r') as g:
            result = g.read()
        self.assertEqual(result, 'Six people were killed and')
        os.remove(filename)
        os.remove(result_filename)
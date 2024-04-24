import os
import unittest

from src.Tools import key_generate


class TestTools(unittest.TestCase):

    def test_key_generate_with_key_extension(self):
        filename = 'temp000.key'
        result = key_generate(filename)
        self.assertEqual(result, filename)
        os.remove(result)

    def test_key_generate_with_no_key_extension(self):
        filename = 'temp000'
        result = key_generate(filename)
        self.assertEqual(result, filename + '.key')
        os.remove(result)

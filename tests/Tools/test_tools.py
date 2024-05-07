import os
import unittest

from src.Tools import key_generate, get_new_filename, write_bytes_to_file


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

    def test_get_new_filename(self):
        result = get_new_filename('tst')
        self.assertFalse(os.path.exists(result))
        self.assertTrue(result.endswith('tst'))

    def test_get_two_new_filename(self):
        result1 = get_new_filename('tst')
        with open(result1, 'w') as f:
            f.write('   ')
        result2 = get_new_filename('tst')
        self.assertNotEqual(result1, result2)
        os.remove(result1)

    def test_write_bytes_to_file(self):
        message = 'proba'.encode()
        output_filename = write_bytes_to_file(message, 'tst')
        with open(output_filename, 'rb') as f:
            result = f.read()
        self.assertEqual(message, result)
        os.remove(output_filename)

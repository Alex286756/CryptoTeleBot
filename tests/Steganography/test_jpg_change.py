import os
import unittest
from src.Steganography import JPGChange


class TestJPGChange(unittest.TestCase):

    def test_encoding_and_decoding(self):
        jpg_filename = 'tests/Steganography/dobroe-utro.jpg'
        test_message = 'proba'
        text_filename = 'test.txt'
        with open(text_filename, 'w') as f:
            f.write(test_message)
        picture_coding = JPGChange(jpg_filename)
        output_filename = picture_coding.encoding(text_filename)

        picture_decoding = JPGChange(output_filename)
        new_text_filename = picture_decoding.decoding()
        with open(new_text_filename, 'r') as f:
            message = f.read()
        self.assertEqual(test_message, message)
        os.remove(new_text_filename)
        os.remove(output_filename)
        os.remove(text_filename)

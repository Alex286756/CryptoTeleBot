import os
import unittest
from src.Steganography import BMPChange


class TestBMPChange(unittest.TestCase):

    def test_get_decode_filename(self):
        filename = 'input.bmp'
        picture = BMPChange(filename)
        output_filename = picture.get_decode_filename()
        self.assertEqual(output_filename, 'input_decode.txt')

    def test_encoding_and_decoding(self):
        bmp_filename = 'tests/Steganography/Rainier.bmp'
        test_message = 'proba'
        text_filename = 'test.txt'
        with open(text_filename, 'w') as f:
            f.write(test_message)
        picture_coding = BMPChange(bmp_filename)
        output_filename = picture_coding.encoding(text_filename)

        picture_decoding = BMPChange(output_filename)
        new_text_filename = picture_decoding.decoding()
        with open(new_text_filename, 'r') as f:
            message = f.read()
        self.assertEqual(test_message, message)
        os.remove(new_text_filename)
        os.remove(output_filename)
        os.remove(text_filename)

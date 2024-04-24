import unittest
from src.Steganography import BMPChange


class TestBMPChange(unittest.TestCase):

    def test_get_decode_filename(self):
        filename = 'input.bmp'
        picture = BMPChange(filename)
        output_filename = picture.get_decode_filename()
        self.assertEqual(output_filename, 'input_decode.txt')

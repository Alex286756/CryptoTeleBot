from typing import Optional

from src.Crypto import Caesar
from src.Tools.constants import Constants
from src.Tools import write_message_to_file


class CaesarHack:
    """
    В классе осуществляется вся работа с фреймом, на котором определяются параметры
    для шифрования/расшифрования текста в изображениях.
    В рамках проекта предполагается, что сообщение написано на одном языке (русском или английском).

    Атрибуты:
    ---------
    alphabet :
        Русский и английский алфавиты.
    frequency :
        Статистическая частота букв в текстах на русском и английском алфавитах.
    alphabet_norm :
        "Вес" статистичесих данных (для нормализации частот).
    alphabet_index :
        Индекс, указывающий на номер алфавита, используемого для расшифрования текста.

    Методы:
    ---------
    __init__():
        Инициализирует начальные данные.
    caesar_hacker(filename: str):
        Взламывает сообщение, зашифрованное шифром Цезаря.
    get_frequency(message):
        Вычисляет и нормализует частоты букв в предоставленном тексте.
    calc_best_shift(cipher_frequency):
        Вычисляет наименьшую разницу между частотами букв в тексте и в исходных данных.
    set_language_index(text):
        По первой букве в тексте сообщения определяет язык и устанавливает соответствующий alphabet_index.
    """

    def __init__(self):
        """
        Инициализирует начальные данные.
        В русском алфавите частота букв 'е' и 'ё' посчитана вместе, также сделано для букв 'ь' и 'ъ'.
        Данные по частотам букв взяты со следующего источника:
        http://www.statistica.ru/local-portals/data-mining/analiz-tekstov/
        """
        self.alphabet = [Constants.ALPHABET_RUS_UPPER_31,
                         Constants.ALPHABET_ENG_UPPER]
        self.frequency = [[62, 14, 38, 13, 25, 72, 7, 16, 62, 10,
                           28, 35, 26, 53, 90, 23, 40, 45, 53, 21,
                           2, 9, 4, 12, 6, 3, 16, 14, 3, 6,
                           18],
                          [796, 160, 284, 401, 1286, 262, 199, 539, 777, 16,
                           41, 351, 243, 751, 662, 181, 17, 683, 662, 972,
                           248, 115, 180, 17, 152, 5]]
        self.alphabet_norm = [sum(self.frequency[0]), sum(self.frequency[1])]
        self.alphabet_index = -1

    def caesar_hacker(self, filename: str) -> Optional[str]:
        """
        Взламывает сообщение, зашифрованное шифром Цезаря (чем длиннее сообщение, тем точнее результат).
        :param filename:
            Имя файла с входящим (зашифрованным сообщением).
        :return:
            Имя файла с расшифрованным сообщением.
        """
        with open(filename, "r", encoding="utf-8") as f:
            ciphertext = f.read()

        modified_text = (((ciphertext.replace('ё', 'е')
                         .replace('Ё', 'Е'))
                         .replace('ъ', 'ь'))
                         .replace('Ъ', 'Ь'))
        self.set_language_index(modified_text)
        if self.alphabet_index == -1:
            return None

        cipher_frequency = self.get_frequency(modified_text)
        best_shift = self.calc_best_shift(cipher_frequency)
        caesar = Caesar(best_shift)
        decrypt_message = caesar.decoding(ciphertext)
        return write_message_to_file(decrypt_message)

    def get_frequency(self, message: str) -> list[int]:
        """
        Вычисляет и нормализует частоты букв в предоставленном тексте.
        :param message: 
            Текст зашифрованного сообщения.
        :return: 
            Список полученных частот по буквам в алфавитном порядке.
        """
        cipher_frequency = [message.upper().count(alpha)
                            for alpha in self.alphabet[self.alphabet_index]]

        total_count = sum(cipher_frequency)
        for i in range(len(cipher_frequency)):
            cipher_frequency[i] = cipher_frequency[i] * self.alphabet_norm[self.alphabet_index] // total_count
        return cipher_frequency

    def calc_best_shift(self, cipher_frequency: list[int]) -> int:
        """
        Вычисляет наименьшую разницу между частотами букв в тексте и в исходных данных.
        :param cipher_frequency:
            Список частот букв в тексте (в алфавитном порядке)
        :return:
            Смещение, при котором частоты максимально совпадают с исходными (ключ шифра).
        """
        best_match = sum(cipher_frequency)
        best_shift = 0
        for shift in range(len(self.alphabet[self.alphabet_index])):
            cipher_frequency_after_shift = cipher_frequency[shift:] + cipher_frequency[:shift]
            difference = [abs(cipher_frequency_after_shift[index] - self.frequency[self.alphabet_index][index])
                          for index in range(len(cipher_frequency_after_shift))]
            total_difference = sum(difference)
            if total_difference < best_match:
                best_match = total_difference
                best_shift = shift
        return best_shift

    def set_language_index(self, text: str) -> None:
        """
        По первой букве в тексте сообщения определяет язык и устанавливает соответствующий alphabet_index.
        :param text:
            Текст сообщения
        """
        is_lang_definition = True
        char_index = 0
        while is_lang_definition and char_index < len(text):
            char = text[char_index].upper()
            if char in self.alphabet[0]:
                self.alphabet_index = 0
                is_lang_definition = False
            elif char in self.alphabet[1]:
                self.alphabet_index = 1
                is_lang_definition = False
            char_index += 1

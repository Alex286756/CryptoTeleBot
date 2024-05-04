from typing import Optional, Union

from src.MyTelebot.constants import Constants


class AbstractCrypto:
    """
    Абстрактный класс для создания классов, реализующих шифры Цезаря, Виженера и Вернама. \n

    Атрибуты:
    ---------
    ENCODE :
        Константа, обозначающая шифрование.
    DECODE :
        Константа, обозначающая расшифрование.
    alphabets :
        Русский и английский алфавиты.
    key :
        Ключ шифра.
    key_index :
        Указатель на символ ключа, который был использован последним (при старте равен -1).

    Методы:
    ---------
    __init__(key: any = None):
        Инициализация начальных параметров.
    get_new_text(old_text, rotation):
        Обработка сообщения в соответствии с параметром rotation.
    encoding(text):
        Запуск процесса шифрования.
    decoding(text):
        Запуск процесса расшифрования.
    check_key(old_text: str) -> None:
        Проверяет соответствие длины и выбранного алфавита полученному сообщению.
        При необходимости удлиняет ключ путем повторения первоначального ключа.
    get_new_char(old_char, rotation):
        Вычисляет результат шифрования/расшифрования символа.
    """

    ENCODE = 1
    DECODE = -1

    def __init__(self, key: Optional[Union[int, str]] = None):
        """
        Инициализация начальных параметров.
        :param key:
            Ключ для шифрования/расшифрования.
        """
        self.alphabets = []
        self.alphabets.append(Constants.ALPHABET_RUS_LOWER + 'ё')
        self.alphabets.append(Constants.ALPHABET_RUS_UPPER + 'Ё')
        self.alphabets.append(Constants.ALPHABET_ENG_LOWER)
        self.alphabets.append(Constants.ALPHABET_ENG_UPPER)
        self.key_index = -1
        self.key = key

    def get_new_char(self, old_char: str, rotation: int) -> str:
        """
        Абстрактный метод, реализация которого будет зависеть от конкретного шифра.
        :param old_char:
            Символ для обработки.
        :param rotation:
            Направление работы шифра
        :return:
            Символ после обработки.
        """
        raise NotImplementedError("Subclasses must implement get new char")

    def get_new_text(self, old_text: str, rotation: int) -> str:
        """
        Обработка сообщения с использованием шифра путем посимвольного шифрования/расшифрования.
        :param old_text:
            Сообщения для обработки.
        :param rotation:
            Направление работы шифра.
        :return:
            Сообщение после обработки.
        """
        self.key_index = -1
        self.check_key(old_text)
        new_text = ''
        for char in old_text:
            new_text += self.get_new_char(char, rotation)
        return new_text

    def encoding(self, text: str) -> str:
        """
        Запуск шифрования.
        :param text:
            Сообщение для зашифрования.
        :return:
            Сообщение после зашифрования.
        """
        return self.get_new_text(text, self.ENCODE)

    def decoding(self, text: str) -> str:
        """
        Запуск расшифрования.
        :param text:
            Сообщение для расшифрования.
        :return:
            Сообщение после расшифрования.
        """
        return self.get_new_text(text, self.DECODE)

    def check_key(self, old_text: str) -> None:
        """
        Проверяет соответствие длины и выбранного алфавита полученному сообщению.\n
        Сначала определяет алфавит по первой букве сообщения и
        удаляет другой алфавит (для ускорения шифрования/расшифрования).\n
        Затем при необходимости удлиняет ключ путем повторения первоначального ключа.

        :param old_text:
            Текст сообщения, поступившего на обработку.
        """
        is_lang_definition = True
        char_index = 0
        while is_lang_definition and char_index < len(old_text):
            char = old_text[char_index]
            if char.lower() in self.alphabets[0]:
                if self.key is None:
                    self.key = 'шефвзъярентчкщипцысэхомгудбайжюль'
                self.alphabets.pop(2)
                self.alphabets.pop(2)
                is_lang_definition = False
            elif char.lower() in self.alphabets[2][:26]:
                if self.key is None:
                    self.key = 'thefiveboxingwizardsjumpquickly'
                self.alphabets.pop(0)
                self.alphabets.pop(0)
                is_lang_definition = False
            char_index += 1

from typing import Optional

from src.Abstract import AbstractCrypto
from src.Tools.constants import Constants


class Vernam(AbstractCrypto):
    """
    Класс для зашифрования/расшифрования текста шифром Вернама. \n
    Наследуется от класса AbstractCrypto.\n
    В рамках проекта считается, что входящее сообщение написано на одном языке. \n
    Язык (поддерживаются русский и английский) определяется по первому символу сообщения.

    Метод:
    ---------
        __init__(self, key: any = None):
            При создании объекта класса корректирует алфавиты.

        get_new_char(old_char, rotation):
            Вычисляет результат шифрования/расшифрования символа.
    """

    def __init__(self, key: Optional[str] = None):
        """
        С учетом того, что шифр Вернама работает побитово, для получения зрелищности в рамках проекта
        алфавиты сделаны размером в 32 символа (в русском алфавите убрана буква ё, к английскому алфавиту
        добавлены отдельные знаки препинания.

        :param key:
            Ключ для шифрования/расшифрования.
        """
        super().__init__(key)
        self.alphabets[0] = Constants.ALPHABET_RUS_LOWER
        self.alphabets[1] = Constants.ALPHABET_RUS_UPPER
        self.alphabets[2] = Constants.ALPHABET_ENG_LOWER + ' .,:;-'
        self.alphabets[3] = Constants.ALPHABET_ENG_UPPER + ' .,:;-'

    def get_new_char(self, old_char: str, rotation: int) -> str:
        """
        Вычисляет результат шифрования/расшифрования символа.\n
        Определяет, является ли символ буквой русского или английского алфавита
        и вычияляет результат в зависимости от алфавита.\n
        Если символ не является буквой русского или английского алфавита,
        то он возвращается без изменений.

        :param old_char:
            символ для обработки

        :param rotation:
            направление движения по алфавиту. Вместе с тем, так как шифр Вернама работает через XOR,
            то значение rotation не играет роли в шифровании/расшифровании.

        :return:
            Символ после применнения шифра Вернама.
        """

        for alphabet in self.alphabets:
            if old_char in alphabet:
                self.key_index = (self.key_index + 1) % len(self.key)
                index_1 = alphabet.index(old_char)
                index_2 = alphabet.lower().index(self.key[self.key_index].lower())
                index_fin = (index_1 ^ index_2) % len(alphabet)
                return alphabet[index_fin]
        return old_char

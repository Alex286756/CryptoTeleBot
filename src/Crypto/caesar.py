from typing import Optional

from src.Abstract import AbstractCrypto


class Caesar(AbstractCrypto):
    """
    Класс для зашифрования/расшифрования текста шифром Цезаря.
    Наследуется от класса AbstractCrypto.

    Атрибут:
    ---------
        key : int
            Ключ шифра (размер сдвига по алфавиту).

    Метод:
    ---------
        get_new_char(old_char, rotation):
            Вычисляет результат шифрования/расшифрования символа.
    """

    def __init__(self, key: Optional[int] = None):
        """
        Устанавливает начальные атрибуты.
        Если ключ не задан, то присваивается ключ, равный 3.

        :param key:
            Ключ шифра (по умолчанию None).
        """
        super().__init__()
        self.key = 3 if key is None else key

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
            направление движения по алфавиту. Принимает одно из двух значений:
            ENCODE = 1      - зашифрование,
            DECODE = -1     - расшифрование.

        :return:
            Символ после применнения шифра Цезаря.
        """
        for alphabet in self.alphabets:
            if old_char in alphabet:
                return alphabet[(alphabet.index(old_char) + rotation * self.key) % len(alphabet)]
        return old_char

    def check_key(self, old_text: str) -> None:
        """
        Перегружает абстрактный метод, т.к. для шифра Цезаря определение алфавита не требуется.
        """
        pass

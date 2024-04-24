from src.Abstract import AbstractCrypto


class Vijener(AbstractCrypto):
    """
    Класс для зашифрования/расшифрования текста шифром Виженера. \n
    Наследуется от класса AbstractCrypto.\n
    В рамках проекта считается, что входящее сообщение написано на одном языке. \n
    Язык (поддерживаются русский и английский) определяется по первому символу сообщения.

    Метод:
    ---------
        get_new_char(old_char, rotation):
            Вычисляет результат шифрования/расшифрования символа.
    """

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
            Символ после применнения шифра Вернама.
        """

        for alphabet in self.alphabets:
            if old_char in alphabet:
                self.key_index = (self.key_index + 1) % len(self.key)
                step = alphabet.lower().index(self.key[self.key_index].lower())
                return alphabet[(alphabet.index(old_char) + rotation * step) % len(alphabet)]
        return old_char

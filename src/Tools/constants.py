import string


class Constants:
    """
    Инициализация необходимых констант для бота
    """
    ENCODE: str = 'ENCODE'
    DECODE: str = 'DECODE'
    HACKING: str = 'HACKING'
    TEXT: str = 'TEXT'
    BMP: str = 'BMP'
    JPG: str = 'JPG'
    PNG: str = 'PNG'
    CAESAR: str = 'CAESAR'
    VIJENER: str = 'VIJENER'
    VERNAM: str = 'VERNAM'
    """
    Сообщения для бота
    """
    INPUT_TEXT_MESSAGE: str = 'Теперь введите сообщение для обработки вручную или пришлите файл в формате txt'
    RESTART_MESSAGE: str = 'Для того, чтобы начать работать сначала, нажмите /start'
    """
    Инициализация алфавитов для текстовых алгоритмов
    """
    ALPHABET_ENG_LOWER: str = string.ascii_letters[:26]
    ALPHABET_ENG_UPPER: str = string.ascii_letters[26:]
    ALPHABET_RUS_LOWER: str = ''.join(map(chr, range(ord('а'), ord('я')+1)))
    ALPHABET_RUS_UPPER: str = ''.join(map(chr, range(ord('А'), ord('Я')+1)))
    ALPHABET_RUS_UPPER_31: str = ALPHABET_RUS_UPPER.replace('Ъ', '')
    """
    Остальные константы
    """
    DEFAULT_KEY_FILENAME = 'default.key'

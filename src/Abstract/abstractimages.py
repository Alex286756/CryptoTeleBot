from src.Tools.constants import Constants


class AbstractImages:
    """
    Абстрактный класс для создания классов, реализующих шифры Цезаря, Виженера и Вернама. \n

    Атрибуты:
    ---------
    in_filename :
        Имя файла c изображением, который будет обрабатывать алгоритм.
    out_filename :
        Имя файла c изображением после применения алгоритма стеганографии.
    key_filename :
        Имя файла с ключом (для алгоритма стеганографии файлов .png).
    key_index :
        Указатель на символ ключа, который был использован последним (при старте равен -1).

    Методы:
    ---------
    __init__(key: any = None):
        Инициализация начальных параметров.
    encoding(message):
        Запуск процесса шифрования сообщения в файл изображения.
    decoding():
        Запуск процесса расшифрования сообщения из файла изображения.
    get_decode_filename():
        Возвращает имя файла, где будет записано расщифрованное сообщение.
    """

    def __init__(self, input_filename: str, key_filename: str = Constants.DEFAULT_KEY_FILENAME):
        """
        Инициализация начальных атрибутов
        :param input_filename:
            Имя файла c изображением, который будет обрабатывать алгоритм.
        :param key_filename:
            Имя файла с ключом (для алгоритма стеганографии файлов .png).
        """
        self.key_index = -1
        self.in_filename = input_filename
        self.out_filename = input_filename[:len(input_filename)-4] + "_out" + input_filename[len(input_filename)-4:]
        self.key_filename = key_filename

    def encoding(self, message_filename: str) -> str:
        """
        Абстрактный метод, реализация которого будет зависеть от конкретного шифра.
        :param message_filename:
            Имя файла с сообщением, которое надо 'спрятать' в изображении.
        :return:
            Возвращает имя файла изображения после обработки.
        """
        raise NotImplementedError("Subclasses must implement encoding")

    def decoding(self) -> str:
        """
        Абстрактный метод, реализация которого будет зависеть от конкретного шифра.
        :return:
            Имя файла с сообщением, полученном после обработки изображения.
        """
        raise NotImplementedError("Subclasses must implement decoding")

    def get_decode_filename(self) -> str:
        """
        По имение файла, записанному в атрибуте in_filename генерирует имя файла, в который будет
        записан результат расшифровки изображения.
        :return:
            Имя файла для записи результата расщифровки.
        """
        return self.in_filename[:len(self.in_filename)-4] + "_decode.txt"

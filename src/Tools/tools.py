import os
from steganocryptopy.steganography import Steganography as StegoCript


def get_new_filename(extension: str) -> str:
    """
    Генерирует имя файла (несуществующего).
    :param extension:
        Расширение, которое должен иметь файл
    :return:
        Имя файла
    """
    filename = 'temp'
    index = 1
    new_filename = filename + str(index) + '.' + extension
    while os.path.isfile(new_filename):
        index += 1
        new_filename = filename + str(index) + '.' + extension
    return new_filename


def write_bytes_to_file(input_bytes: bytes, extension: str) -> str:
    """
        Записывает набор байтов в файл.
    :param input_bytes:
        Байты для записи
    :param extension:
        Расширение, которое должен иметь файл
    :return:
        Имя файла
    """
    message_filename = get_new_filename(extension)
    with open(message_filename, "wb") as f:
        f.write(input_bytes)
    return message_filename


def write_message_to_file(input_text: str) -> str:
    """
    Записывает текст в файл.
    :param input_text:
        Текст для записи
    :return:
        Имя файла с текстом
    """
    message_filename = get_new_filename('txt')
    with open(message_filename, "w", encoding='utf-8') as f:
        f.write(input_text)
    return message_filename


def key_generate(filename: str) -> str:
    """
    Генерирует ключ для стеганографии и записывает его в файл.

    :param filename:
        Имя файла, в котором надо сохранить ключ. Метод устанавливает расширение файла '.key'.
    :return:
        Имя файла с ключом.
    """
    index = filename.rfind('.')
    if index != -1:
        key_filename = filename[:index] + ".key"
    else:
        key_filename = filename + ".key"
    StegoCript.generate_key(key_filename)
    return key_filename

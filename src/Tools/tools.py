import os
from tkinter import filedialog
from steganocryptopy.steganography import Steganography as StegoCript


def load_image_file(field_name):
    """
    Запускает окно, предлагающее открыть файл с изображением.
    :param field_name:
        Поле, в которое будет записано имя открываемого файла.
    """
    filetypes = (("Изображение", "*.jpg *.bmp *.png"),)
    filename = filedialog.askopenfilename(title="Выберите исходный файл с изображением",
                                          initialdir="/",
                                          filetypes=filetypes)
    if filename:
        field_name.set(filename)


def load_message_file(field_name):
    """
    Запускает окно, предлагающее открыть файл с текстом.
    :param field_name:
        Поле, в которое будет записано имя открываемого файла.
    """
    filetypes = (("Текстовый файл", "*.txt"),
                 ("Любой", "*"))
    filename = filedialog.askopenfilename(title="Выберите исходный файл с сообщением",
                                          initialdir=os.getcwd(),
                                          filetypes=filetypes)
    if filename:
        field_name.set(filename)


def get_new_filename():
    """
    Генерирует имя файла (несуществующего).
    :return:
        Имя файла
    """
    filename = 'temp'
    index = 1
    new_filename = filename + str(index) + '.txt'
    while os.path.isfile(new_filename):
        index += 1
        new_filename = filename + str(index) + '.txt'
    return new_filename


def write_bytes_to_file(input_bytes):
    """
    Pаписывает набор байтов в файл.
    :param input_bytes:
        Байты для записи
    :return:
        Имя файла
    """
    message_filename = get_new_filename()
    with open(message_filename, "wb") as f:
        f.write(input_bytes)
    return message_filename


def write_message_to_file(input_text):
    """
    Записывает текст в файл.
    :param input_text:
        Текст для записи
    :return:
        Имя файла с текстом
    """
    message_filename = get_new_filename()
    with open(message_filename, "w", encoding='utf-8') as f:
        f.write(input_text)
    return message_filename


def key_generate(filename):
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


def get_key_filename(field_name):
    """
    Запускает окно, предлагающее открыть файл с ключом.
    :param field_name:
        Поле, в которое будет записано имя открываемого файла.
    """
    filetypes = (("Файлы с ключом", "*.key"),
                 ("Любой", "*"))
    filename = filedialog.askopenfilename(title="Выберите файл с ключом",
                                          initialdir="/",
                                          filetypes=filetypes)
    if filename:
        field_name.set(filename)

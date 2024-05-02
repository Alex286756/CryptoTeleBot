import os
import zlib

from cryptography.fernet import InvalidToken
import telebot
from telebot import types

from src.Crypto import Caesar, Vijener, Vernam
from src.Hacking import CaesarHack
from src.MyTelebot.constants import Constants
from src.Steganography import BMPChange, JPGChange, PNGChange
from src.Tools import write_bytes_to_file, write_message_to_file
from src.Tools.tools import get_new_filename, key_generate

"""
Инициализация необходимых режимов
"""
target = None
source = None
input_text = None
code = Caesar
key = None
need_key_file = False
key_filename = 'private.key'

"""
Инициализация Телеграм-бота по токену, записанному в файле token.txt
"""
with open('token.txt') as f:
    token = f.readline().strip()
bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def start_message(message):
    """
        Обработка команды '/start' в чате.
        Выдает в чат возможные режимы работы программы (шифрование, расшифрование, взлом шифра Цезаря).

    :param message:
        Сообщение '/start', по которому бот определяет id чата и имя пользователя.
    """
    global target, source, code, input_text, key, need_key_file, key_filename
    target = None
    source = None
    input_text = None
    key = None
    need_key_file = False
    key_filename = 'private.key'
    chat_id = message.chat.id
    first_name = message.chat.first_name
    inline_markup = types.InlineKeyboardMarkup(row_width=True)
    inline_keyboard_encode = types.InlineKeyboardButton('Шифровать', callback_data=Constants.ENCODE)
    inline_keyboard_decode = types.InlineKeyboardButton('Расшифровать', callback_data=Constants.DECODE)
    inline_keyboard_hack = types.InlineKeyboardButton('Взломать шифр Цезаря', callback_data=Constants.HACKING)
    inline_markup.add(inline_keyboard_encode, inline_keyboard_decode, inline_keyboard_hack)
    bot.send_message(chat_id, f"Привет, {first_name}, чем я могу тебе помочь? "
                              f"Для получения расширенной помощи введи команду /help", reply_markup=inline_markup)


@bot.message_handler(commands=["help"])
def help_message(message):
    """
        Выдает подсказку по работе с ботом.
    :param message:
        Содержит данные сообщения, откуда пришел вызов.
    """
    chat_id = message.chat.id
    bot.send_message(chat_id, "Данный телеграмм-бот создан для шифрования/расшифрования текстовых сообщений "
                              "шифрами Цезаря, Виженера, Вернама, а также зашифрования/расшифрования "
                              "сообщений внутри bmp-, jpg-, png-изображений. Кроме того, в качестве фан-бонуса "
                              "он умеет взламывать шифр Цезаря, т.е. при отсутствии ключа восстановить "
                              "исходное сообщение." )
    bot.send_message(chat_id, "В рамках проекта имеются несколько ограничений. ")
    bot.send_message(chat_id, "1. Шифрование/расшифрование текстовых сообщений внутри изображений "
                              "осуществляется только текста на английском языке.")
    bot.send_message(chat_id, "2. При использовании шифра Вернама ключ должен быть длиною не "
                              "меньше шифруемого текста.")
    bot.send_message(chat_id, "3. При передаче файлов изображений необходимо учесть, что при сжатии файлов "
                              "может произойти потеря информации. Поэтому изображения требуется передавать боту "
                              "без сжатия (как документ).")
    bot.send_message(chat_id, "Для старта работы напишите /start")


def sources_menu(chat_id, message_id, dist):
    """
        Метод выводит в чат возможные варианты исходных данных для обработки
    :param chat_id:
        Id чата, куда надо вывести кнопки
    :param message_id:
        Id сообщения, содержащего предыдущие кнопки (лишние убираются чтобы не путать пользователя
    :param dist:
        Направление работы программы (зашифрование, расшифрование, взлом)
    """
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f'Значит, будем {dist}...')
    inline_markup = types.InlineKeyboardMarkup(row_width=True)
    inline_keyboard_text = types.InlineKeyboardButton('текст', callback_data=Constants.TEXT)
    inline_keyboard_bmp = types.InlineKeyboardButton('bmp-изображение', callback_data=Constants.BMP)
    inline_keyboard_jpg = types.InlineKeyboardButton('jpg-изображение', callback_data=Constants.JPG)
    inline_keyboard_png = types.InlineKeyboardButton('png-изображение', callback_data=Constants.PNG)
    inline_markup.add(inline_keyboard_text, inline_keyboard_bmp, inline_keyboard_jpg, inline_keyboard_png)
    bot.send_message(chat_id, f"Что будем {dist}?", reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda call: call.data == Constants.ENCODE)
def set_target_to_encode(call):
    """
        Метод выполняется после выбора направления работы программы "Зашифрование". Сохраняет данные об этом в
        глобальной переменной target и вызывает набор кнопок для дальнейшей работы.
    :param call:
        Содержит данные, откуда пришел вызов.
    """
    global target
    chat_id = call.message.chat.id
    target = Constants.ENCODE
    sources_menu(chat_id, call.message.id, 'шифровать')


@bot.callback_query_handler(func=lambda call: call.data == Constants.DECODE)
def set_target_to_decode(call):
    """
        Метод выполняется после выбора направления работы программы "Расшифрование". Сохраняет данные об этом в
        глобальной переменной target и вызывает набор кнопок для дальнейшей работы.
    :param call:
        Содержит данные, откуда пришел вызов.
    """
    global target
    chat_id = call.message.chat.id
    target = Constants.DECODE
    sources_menu(chat_id, call.message.id, 'расшифровывать')


@bot.callback_query_handler(func=lambda call: call.data == Constants.TEXT)
def set_source_to_text(call):
    """
        Метод выполняется после выбора источника данных "Текст". Сохраняет данные об этом в
        глобальной переменной source и вызывает набор кнопок для выбора метода шифрования.
    :param call:
        Содержит данные, откуда пришел вызов.
    """
    global source
    chat_id = call.message.chat.id
    source = Constants.TEXT
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.id, text='Текст так текст...')
    inline_markup = types.InlineKeyboardMarkup(row_width=True)
    inline_keyboard_caesar = types.InlineKeyboardButton('Шифр Цезаря', callback_data=Constants.CAESAR)
    inline_keyboard_vijener = types.InlineKeyboardButton('Шифр Виженера', callback_data=Constants.VIJENER)
    inline_keyboard_vernam = types.InlineKeyboardButton('Шифр Вернама', callback_data=Constants.VERNAM)
    inline_markup.add(inline_keyboard_caesar, inline_keyboard_vijener, inline_keyboard_vernam)
    bot.send_message(chat_id, "Какой шифр будем использовать?", reply_markup=inline_markup)


@bot.message_handler(content_types=['text'],
                     func=lambda message: source == Constants.TEXT and key is None)
def get_key_for_textcode(message):
    """
        Метод выполняется при вводе текста с клавиатуры после выбора источника данных "Текст", но ключ для
        шифрования/расшифрования еще не определен.

        Полученный текст программа считает ключом и записывает в глобальную переменную key.

        После этого предлагается пользователю ввести текст сообщения (вручную или прислать файл).
    :param message:
        Содержит данные сообщения, откуда пришел вызов.
    """
    global key, code
    coding = code(key)
    chat_id = message.chat.id
    if isinstance(coding, Caesar):
        if message.text.isdigit():
            key = int(message.text)
            bot.send_message(chat_id,
                             'Теперь введите сообщение для обработки вручную или пришлите файл в формате txt')
        else:
            bot.send_message(chat_id, 'Нужно ввести просто число!')
    elif isinstance(coding, Vijener) or isinstance(coding, Vernam):
        if message.text.isalpha():
            key = message.text
            bot.send_message(chat_id,
                             'Теперь введите сообщение для обработки вручную или пришлите файл в формате txt')
        else:
            bot.send_message(chat_id, 'Нужно ввести просто набор символов того алфавита, '
                                      'на котором написано сообщение!')
    else:
        bot.send_message(chat_id, 'Что-то пошло не так (не определен шифр для обработки текста).'
                                  'Давайте начнем сначала? Нажмите /start')


@bot.message_handler(content_types=['document'],
                     func=lambda message: source == Constants.TEXT and key is None)
def get_file_with_key_for_textcode(message):
    """
        Метод выполняется при получении файла с ключом после выбора источника данных "Текст", но ключ для
        шифрования/расшифрования еще не определен.

        Текст из файла программа считает ключом и записывает в глобальную переменную key.

        После этого предлагается пользователю ввести текст сообщения (вручную или прислать файл).
    :param message:
        Содержит данные сообщения, откуда пришел вызов.
    """
    global key, code
    coding = code(key)
    chat_id = message.chat.id
    file_in = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_in.file_path)
    input_key = downloaded_file.decode()
    if isinstance(coding, Caesar):
        res = ''.join([el for el in input_key if el.isdigit()])
        key = int(res)
    elif isinstance(coding, Vijener) or isinstance(coding, Vernam):
        res = ''.join([el for el in input_key if el.isalpha()])
        key = int(res)
    else:
        bot.send_message(chat_id, 'Что-то пошло не так (не определен шифр для обработки текста).'
                                  'Давайте начнем сначала? Нажмите /start')


@bot.message_handler(content_types=['document'],
                     func=lambda message: source == Constants.TEXT and key is not None)
def get_file_for_textcode(message):
    """
        Метод выполняется при получении файла с текстом сообщения после выбора источника данных "Текст" и
        получения ключа.

        Текст из файла программа считывается и обрабатывается в зависимости от значения глобальной переменной target.

        Результат обработки направляется пользователю в виде текстового файла.

    :param message:
        Содержит данные сообщения, откуда пришел вызов.
    """
    chat_id = message.chat.id
    file_in = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_in.file_path)
    input_message = downloaded_file.decode()
    result_filename = get_new_filename('txt')
    coding = code(key)
    result = input_message
    if target == Constants.DECODE:
        result = coding.decoding(input_message)
    elif target == Constants.ENCODE:
        result = coding.encoding(input_message)
    bot.send_message(chat_id, 'Результат обработки в файле')
    bot.send_document(chat_id, result.encode('utf-8'), visible_file_name=result_filename)
    if os.path.exists(result_filename):
        os.remove(result_filename)
    bot.send_message(chat_id, 'Для того, чтобы начать работать сначала, нажмите /start')


@bot.message_handler(content_types=['text'],
                     func=lambda message: source == Constants.TEXT and key is not None)
def get_text_for_textcode(message):
    """
        Метод выполняется при вводе с клавиатуры текста сообщения после выбора источника данных "Текст" и
        получения ключа.

        Текст обрабатывается в зависимости от значения глобальной переменной target.

        Результат обработки направляется пользователю сообщением.

    :param message:
        Содержит данные сообщения, откуда пришел вызов.
    """
    chat_id = message.chat.id
    coding = code(key)
    result = message.text
    if target == Constants.DECODE:
        result = coding.decoding(message.text)
    elif target == Constants.ENCODE:
        result = coding.encoding(message.text)
    bot.send_message(chat_id, 'Вот результат обработки сообщения:')
    bot.send_message(chat_id, result)
    bot.send_message(chat_id, 'Для того, чтобы начать работать сначала, нажмите /start')


@bot.callback_query_handler(func=lambda call: call.data == Constants.CAESAR)
def set_code_to_caesar(call):
    """
        Метод выполняется после выбора шифра Цезаря. Сохраняет данные об этом в
        глобальной переменной code и предлагает ввести ключ для дальнейшей работы шифра.
    :param call:
        Содержит данные, откуда пришел вызов.
    """
    global code, key
    chat_id = call.message.chat.id
    code = Caesar
    key = None
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.id, text='Шифр Цезаря, хороший выбор')
    bot.send_message(chat_id, 'Введите ключ (число, равное сдвигу по алфавиту), '
                              'с помощью которого мы будем обрабатывать сообщение, '
                              'вручную или пришлите файл (ВНИМАНИЕ! Будут использованы только '
                              'цифры):')


@bot.callback_query_handler(func=lambda call: call.data == Constants.VIJENER)
def set_code_to_vijener(call):
    """
        Метод выполняется после выбора шифра Виженера. Сохраняет данные об этом в
        глобальной переменной code и предлагает ввести ключ для дальнейшей работы шифра.
    :param call:
        Содержит данные, откуда пришел вызов.
    """
    global code, key
    chat_id = call.message.chat.id
    code = Vijener
    key = None
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.id,
                          text='Шифр Виженера, лучше чем просто шифр Цезаря!')
    bot.send_message(chat_id, 'Введите ключ (набор символов), '
                              'с помощью которого мы будем обрабатывать сообщение, '
                              'вручную или пришлите файл (ВНИМАНИЕ! Будут использованы только '
                              'буквы):')


@bot.callback_query_handler(func=lambda call: call.data == Constants.VERNAM)
def set_code_to_vernam(call):
    """
        Метод выполняется после выбора шифра Вернама. Сохраняет данные об этом в
        глобальной переменной code и предлагает ввести ключ для дальнейшей работы шифра.
    :param call:
        Содержит данные, откуда пришел вызов.
    """
    global code, key
    chat_id = call.message.chat.id
    code = Vernam
    key = None
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.id,
                          text='Шифр Вернама, лучшее из того, что я умею!!!')
    bot.send_message(chat_id, 'Введите ключ (набор символов), '
                              'с помощью которого мы будем обрабатывать сообщение, '
                              'вручную или пришлите файл (ВНИМАНИЕ! Будут использованы только '
                              'буквы):')


def steganography_start(chat_id, file_type):
    """
        Выдает в чат предложение прислать изображение в качестве исходного для обработки.
    :param chat_id:
        Id чата, в котором происходит общение
    :param file_type:
        Тип файла с исходными данными
    """
    bot.send_message(chat_id, f'Осталось только прислать мне {file_type}-файл для обработки '
                              '(не забудьте снять галочку "сжать изображение")...')


@bot.callback_query_handler(func=lambda call: call.data == Constants.BMP)
def set_source_to_bmp(call):
    """
        Метод выполняется после выбора в качестве исходного файла bmp-изображение. Сохраняет данные об этом в
        глобальной переменной source.

        В случае зашифрования предлагается ввести текст для зашифрования.
        В случае расшифрования выдает предложение прислать файл с изображением.
    :param call:
        Содержит данные, откуда пришел вызов.
    """
    global source
    source = Constants.BMP
    chat_id = call.message.chat.id
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.id,
                          text='Вы выбрали режим работы с bmp-изображением...')
    if target == Constants.ENCODE:
        bot.send_message(chat_id, 'Введите сообщение для зашифрования вручную или пришлите файл с текстом...')
    elif target == Constants.DECODE:
        steganography_start(chat_id, 'BMP')
    else:
        bot.send_message(chat_id, 'Что-то пошло не так (не определен режим работы бота)...'
                                  'Начните сначала, пожалуйста, с команды /start')


@bot.message_handler(content_types=['text'],
                     func=lambda message: target == Constants.ENCODE and source == Constants.BMP)
def text_for_encoding_bmp(message):
    """
        Метод выполняется при вводе с клавиатуры текста сообщения после выбора источника данных
        bmp-изображения и выбора режима зашифрования.

        Текст сохраняется в файл для дальнейшей обработки (имя файла записано в переменной input-text).

    :param message:
        Содержит данные сообщения, откуда пришел вызов.
    """
    global input_text

    chat_id = message.chat.id
    input_text = write_message_to_file(message.text)
    steganography_start(chat_id, 'BMP')


@bot.message_handler(content_types=['document'],
                     func=lambda message: (target == Constants.ENCODE) and
                                          (source == Constants.BMP) and
                                          (message.document.mime_type == 'text/plain'))
def file_with_text_for_encoding_bmp(message):
    """
        Метод выполняется при получении текстового файла после выбора источника данных
        bmp-изображения и выбора режима зашифрования.

        Имя полученного файла записано в глобальной переменной input-text.

    :param message:
        Содержит данные сообщения, откуда пришел вызов.
    """
    global input_text
    chat_id = message.chat.id
    file_in_path = bot.get_file(message.document.file_id).file_path
    downloaded_file = bot.download_file(file_in_path)
    input_text = write_bytes_to_file(downloaded_file, 'txt')
    steganography_start(chat_id, 'BMP')


@bot.message_handler(content_types=['document'], func=lambda message: 'bmp' in message.document.mime_type)
def get_bmp_image(message):
    """
        Метод выполняется при получении bmp-файла.

        В зависимости от значение переменной target производит зашифрование или расшифрование.

    :param message:
        Содержит данные сообщения, откуда пришел вызов.
    """
    global input_text
    chat_id = message.chat.id
    if source == Constants.BMP:
        file_in_path = bot.get_file(message.document.file_id).file_path
        downloaded_file = bot.download_file(file_in_path)
        file_in_filename = write_bytes_to_file(downloaded_file, 'bmp')
        bmp = BMPChange(file_in_filename)
        if target == Constants.DECODE:
            try:
                result_filename = bmp.decoding()
                with open(result_filename, "r", encoding='utf-8') as f_out:
                    result_message = f_out.read()
                    bot.send_message(chat_id, 'Вот что удалось расшифровать:')
                    bot.send_message(chat_id, result_message)
                os.remove(result_filename)
            except IndexError:
                bot.send_message(chat_id, 'Сообщение найти не удалось, к сожалению...')
            finally:
                bot.send_message(chat_id, 'Для того, чтобы начать работать сначала, нажмите /start',
                                 reply_markup=types.ReplyKeyboardRemove())
        elif target == Constants.ENCODE:
            result_filename = bmp.encoding(input_text)
            with open(result_filename, "rb") as f_out:
                result_message = f_out.read()
                bot.send_message(chat_id, 'Вот изображение после обработки:')
                bot.send_document(chat_id, result_message, visible_file_name=result_filename)
            os.remove(result_filename)
            os.remove(str(input_text))
            input_text = None
            bot.send_message(chat_id, 'Для того, чтобы начать работать сначала, нажмите /start',
                             reply_markup=types.ReplyKeyboardRemove())
        os.remove(file_in_filename)
    else:
        match source:
            case Constants.TEXT:
                choice = 'до этого выбрали режим обработки текста'
            case Constants.JPG:
                choice = 'до этого выбрали режим обработки jpg-изображения'
            case Constants.PNG:
                choice = 'до этого выбрали режим обработки png-изображения'
            case _:
                choice = 'что делать с ним не указали'
        bot.send_message(chat_id, f'Вы прислали bmp-изображение, а {choice}! Начните с команды /start, пожалуйста')


@bot.callback_query_handler(func=lambda call: call.data == Constants.JPG)
def set_source_to_jpg(call):
    """
        Метод выполняется после выбора в качестве исходного файла jpg-изображение. Сохраняет данные об этом в
        глобальной переменной source.

        В случае зашифрования предлагается ввести текст для зашифрования.
        В случае расшифрования выдает предложение прислать файл с изображением.
    :param call:
        Содержит данные, откуда пришел вызов.
    """
    global source
    source = Constants.JPG
    chat_id = call.message.chat.id
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.id,
                          text='Вы выбрали режим работы с jpg-изображением...')
    if target == Constants.ENCODE:
        bot.send_message(chat_id, 'Введите сообщение для зашифрования вручную или пришлите файл с текстом...')
    elif target == Constants.DECODE:
        steganography_start(chat_id, 'JPG')
    else:
        bot.send_message(chat_id, 'Что-то пошло не так (не определен режим работы бота)...'
                                  'Начните сначала, пожалуйста, с команды /start')


@bot.message_handler(content_types=['text'],
                     func=lambda message: target == Constants.ENCODE and source == Constants.JPG)
def text_for_encoding_jpg(message):
    """
        Метод выполняется при вводе с клавиатуры текста сообщения после выбора источника данных
        jpg-изображения и выбора режима зашифрования.

        Текст сохраняется в файл для дальнейшей обработки (имя файла записано в переменной input-text).

    :param message:
        Содержит данные сообщения, откуда пришел вызов.
    """
    global input_text

    chat_id = message.chat.id
    input_text = write_message_to_file(message.text)
    steganography_start(chat_id, 'JPG')


@bot.message_handler(content_types=['document'],
                     func=lambda message: (target == Constants.ENCODE) and
                                          (source == Constants.JPG) and
                                          (message.document.mime_type == 'text/plain'))
def file_with_text_for_encoding_jpg(message):
    """
        Метод выполняется при получении текстового файла после выбора источника данных
        jpg-изображения и выбора режима зашифрования.

        Имя полученного файла записано в глобальной переменной input-text.

    :param message:
        Содержит данные сообщения, откуда пришел вызов.
    """
    global input_text
    chat_id = message.chat.id
    file_in_path = bot.get_file(message.document.file_id).file_path
    downloaded_file = bot.download_file(file_in_path)
    input_text = write_bytes_to_file(downloaded_file, 'txt')
    steganography_start(chat_id, 'JPG')


@bot.message_handler(content_types=['document'], func=lambda message: 'jpeg' in message.document.mime_type)
def get_jpg_image(message):
    """
        Метод выполняется при получении jpg-файла.

        В зависимости от значение переменной target производит зашифрование или расшифрование.

    :param message:
        Содержит данные сообщения, откуда пришел вызов.
    """
    chat_id = message.chat.id
    if source == Constants.JPG:
        file_in_path = bot.get_file(message.document.file_id).file_path
        downloaded_file = bot.download_file(file_in_path)
        file_in_filename = write_bytes_to_file(downloaded_file, 'jpg')
        jpg = JPGChange(file_in_filename)
        if target == Constants.DECODE:
            try:
                result_filename = jpg.decoding()
                with open(result_filename, "r", encoding='utf-8') as f_out:
                    result_message = f_out.read()
                    bot.send_message(chat_id, 'Вот что удалось расшифровать:')
                    bot.send_message(chat_id, result_message)
                os.remove(result_filename)
            except zlib.error:
                bot.send_message(chat_id, 'Сообщение найти не удалось, к сожалению...')
            finally:
                bot.send_message(chat_id, 'Для того, чтобы начать работать сначала, нажмите /start',
                                 reply_markup=types.ReplyKeyboardRemove())
        elif target == Constants.ENCODE:
            result_filename = jpg.encoding(input_text)
            with open(result_filename, "rb") as f_out:
                result_message = f_out.read()
                bot.send_message(chat_id, 'Вот изображение после обработки:')
                bot.send_document(chat_id, result_message, visible_file_name=result_filename)
            os.remove(result_filename)
            os.remove(str(input_text))
            bot.send_message(chat_id, 'Для того, чтобы начать работать сначала, нажмите /start',
                             reply_markup=types.ReplyKeyboardRemove())
        os.remove(file_in_filename)
    else:
        match source:
            case Constants.TEXT:
                choice = 'до этого выбрали режим обработки текста'
            case Constants.BMP:
                choice = 'до этого выбрали режим обработки bmp-изображения'
            case Constants.PNG:
                choice = 'до этого выбрали режим обработки png-изображения'
            case _:
                choice = 'что делать с ним не указали'
        bot.send_message(chat_id, f'Вы прислали jpg-изображение, а {choice}! Начните с команды /start, пожалуйста')


@bot.callback_query_handler(func=lambda call: call.data == Constants.PNG)
def set_source_to_png(call):
    """
        Метод выполняется после выбора в качестве исходного файла png-изображение. Сохраняет данные об этом в
        глобальной переменной source.

        В случае зашифрования предлагается ввести текст для зашифрования.
        В случае расшифрования выдает предложение о вводе ключа для расшифрования.
    :param call:
        Содержит данные, откуда пришел вызов.
    """
    global source
    source = Constants.PNG
    chat_id = call.message.chat.id

    bot.edit_message_text(chat_id=chat_id, message_id=call.message.id,
                          text='Вы выбрали режим работы с png-изображением...')
    if target == Constants.ENCODE:
        bot.send_message(chat_id, 'Введите сообщение для зашифрования вручную или пришлите файл с текстом...')
    elif target == Constants.DECODE:
        get_key_menu(chat_id)
    else:
        bot.send_message(chat_id, 'Что-то пошло не так (не определен режим работы бота)...'
                                  'Начните сначала, пожалуйста, с команды /start')


def get_key_menu(chat_id):
    """
        Предлагает пользователю ввести ключ вручную или прислать ключ файлом.

    :param chat_id:
        Id чата, в котором происходит общение.
    """
    global need_key_file
    need_key_file = True
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_default_key = types.KeyboardButton(text='Использовать ключ по умолчанию')
    keyboard_new_key = types.KeyboardButton(text='Сгенерировать новый ключ')
    markup.add(keyboard_default_key, keyboard_new_key)
    bot.send_message(chat_id, 'Введите ключ для обработки png-изображения вручную или пришлите файл с ключом...',
                     reply_markup=markup)


@bot.message_handler(func=lambda message: need_key_file and message.text == 'Использовать ключ по умолчанию')
def use_default_key_for_png(message):
    """
        Вызывается в случае использования ключа по умолчанию (находится в файле private.key)
    для работы с png-изображением.
    :param message:
        Содержит данные сообщения, откуда пришел вызов.
    """
    global need_key_file, key_filename

    chat_id = message.chat.id
    key_filename = 'private.key'
    need_key_file = False
    with open(key_filename, 'rb') as f_key:
        key_file = f_key.read()
        bot.send_message(chat_id, 'Файл с ключом:')
        bot.send_document(chat_id, key_file, visible_file_name=key_filename)
    steganography_start(chat_id, 'PNG')


@bot.message_handler(func=lambda message: need_key_file and message.text == 'Сгенерировать новый ключ')
def generate_new_key_for_png(message):
    """
        Вызывается в случае необходимости генерирования ключа для работы с png-изображением.
    :param message:
        Содержит данные сообщения, откуда пришел вызов.
    """
    global need_key_file, key_filename

    chat_id = message.chat.id
    new_key_filename = get_new_filename('key')
    key_filename = key_generate(new_key_filename)
    need_key_file = False
    with open(key_filename, 'rb') as f_key:
        key_file = f_key.read()
        bot.send_message(chat_id, 'Новый файл с ключом:')
        bot.send_document(chat_id, key_file, visible_file_name=key_filename)
    steganography_start(chat_id, 'PNG')


@bot.message_handler(content_types=['text'],
                     func=lambda message: need_key_file and source == Constants.PNG)
def get_key_for_png(message):
    """
        Метод выполняетсяв в случае ввода ключа для работы с png-изображением вручную. Ключ сохраняется в файл.
    :param message:
        Содержит данные сообщения, откуда пришел вызов.
    """
    global key_filename, need_key_file

    chat_id = message.chat.id
    key_filename = write_message_to_file(message.text)
    need_key_file = False
    steganography_start(chat_id, 'PNG')


@bot.message_handler(content_types=['document'],
                     func=lambda message: need_key_file and (message.document.mime_type == 'text/plain'))
def get_file_with_key_for_png(message):
    """
        Метод выполняетсяв в случае получения файла с ключом для работы с png-изображением.
    :param message:
        Содержит данные сообщения, откуда пришел вызов.
    """
    global key_filename, need_key_file
    key_in_path = bot.get_file(message.document.file_id).file_path
    downloaded_key_file = bot.download_file(key_in_path)
    key_filename = write_bytes_to_file(downloaded_key_file, 'key')
    need_key_file = False
    steganography_start(message.chat.id, 'PNG')


@bot.message_handler(content_types=['text'],
                     func=lambda message: target == Constants.ENCODE and source == Constants.PNG)
def text_for_encoding_png(message):
    """
        Метод выполняетсяв в случае ввода текста сообщения вручную для работы с png-изображением.
    :param message:
        Содержит данные сообщения, откуда пришел вызов.
    """
    global input_text

    chat_id = message.chat.id
    input_text = write_message_to_file(message.text)
    get_key_menu(chat_id)


@bot.message_handler(content_types=['document'],
                     func=lambda message: (target == Constants.ENCODE) and
                                          (source == Constants.PNG) and
                                          (message.document.mime_type == 'text/plain'))
def file_with_text_for_encoding_png(message):
    """
        Метод выполняетсяв в случае получения файла с текстом сообщения для работы с png-изображением.
    :param message:
        Содержит данные сообщения, откуда пришел вызов.
    """
    global input_text
    chat_id = message.chat.id
    file_in_path = bot.get_file(message.document.file_id).file_path
    downloaded_file = bot.download_file(file_in_path)
    input_text = write_bytes_to_file(downloaded_file, 'txt')
    get_key_menu(chat_id)


@bot.message_handler(content_types=['document'], func=lambda message: message.document.mime_type == 'image/png')
def get_png_image(message):
    """
        Метод выполняетсяв в случае получения файла с png-изображением.

        В зависимости от значение переменной target производит зашифрование или расшифрование.
    :param message:
        Содержит данные сообщения, откуда пришел вызов.
    """
    chat_id = message.chat.id
    if source == Constants.PNG:
        file_in_path = bot.get_file(message.document.file_id).file_path
        downloaded_file = bot.download_file(file_in_path)
        file_in_filename = write_bytes_to_file(downloaded_file, 'png')
        png = PNGChange(file_in_filename, key_filename)
        if target == Constants.DECODE:
            try:
                result_filename = png.decoding()
                with open(result_filename, "r", encoding='utf-8') as f_out:
                    result_message = f_out.read()
                    bot.send_message(chat_id, 'Вот что удалось расшифровать:')
                    bot.send_message(chat_id, result_message)
                os.remove(result_filename)
            except InvalidToken:
                bot.send_message(chat_id, 'Сообщение найти не удалось, к сожалению...')
            finally:
                bot.send_message(chat_id, 'Для того, чтобы начать работать сначала, нажмите /start',
                                 reply_markup=types.ReplyKeyboardRemove())
        elif target == Constants.ENCODE:
            result_filename = png.encoding(input_text)
            with open(result_filename, "rb") as f_out:
                result_message = f_out.read()
                bot.send_message(chat_id, 'Вот изображение после обработки:')
                bot.send_document(chat_id, result_message, visible_file_name=result_filename)
            os.remove(result_filename)
            os.remove(str(input_text))
            bot.send_message(chat_id, 'Для того, чтобы начать работать сначала, нажмите /start',
                             reply_markup=types.ReplyKeyboardRemove())
        if key_filename != 'private.key':
            os.remove(key_filename)
        os.remove(file_in_filename)
    else:
        match source:
            case Constants.TEXT:
                choice = 'до этого выбрали режим обработки текста'
            case Constants.JPG:
                choice = 'до этого выбрали режим обработки jpg-изображения'
            case Constants.BMP:
                choice = 'до этого выбрали режим обработки bmp-изображения'
            case _:
                choice = 'что делать с ним не указали'
        bot.send_message(chat_id, f'Вы прислали bmp-изображение, а {choice}! Начните с команды /start, пожалуйста')


@bot.callback_query_handler(func=lambda call: call.data == Constants.HACKING)
def set_target_to_hacking(call):
    """
        Метод выполняется после выбора режима работы "Взлом шифра Цезаря".
    :param call:
        Содержит данные, откуда пришел вызов.
    """
    global target
    chat_id = call.message.chat.id
    target = Constants.HACKING
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.id, text='Значит, будем взламывать ' + '\U0001F609')
    bot.send_message(chat_id, 'Введите сообщение, которое надо взломать, вручную или '
                              'направьте файл с текстом сообщения')


@bot.message_handler(content_types=['document'], func=lambda message: target == Constants.HACKING)
def get_file_for_hacking(message):
    """
        Метод выполняетсяв в случае получения файла для взлома шифра Цезаря.
    :param message:
        Содержит данные сообщения, откуда пришел вызов.
    """
    chat_id = message.chat.id
    try:
        file_in = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_in.file_path)

        src_message = write_bytes_to_file(downloaded_file, 'txt')
        hack = CaesarHack()
        result_filename = hack.caesar_hacker(src_message)
        if os.path.exists(src_message):
            os.remove(src_message)
        with open(result_filename, "rb") as f_out:
            result_message = f_out.read()
        bot.send_document(chat_id, result_message, visible_file_name=result_filename)
        if os.path.exists(result_filename):
            os.remove(result_filename)
    except Exception as e:
        bot.reply_to(message, e.__str__())
    finally:
        bot.send_message(chat_id, 'Для того, чтобы начать работать сначала, нажмите /start',
                         reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(content_types=['text'], func=lambda message: target == Constants.HACKING)
def get_text_for_hacking(message):
    """
        Метод выполняетсяв в случае получения текста сообщения для взлома шифра Цезаря.
    :param message:
        Содержит данные сообщения, откуда пришел вызов.
    """
    # global input_text

    chat_id = message.chat.id
    try:
        src_message = write_message_to_file(message.text)
        hack = CaesarHack()
        result_filename = hack.caesar_hacker(src_message)
        if os.path.exists(src_message):
            os.remove(src_message)
        with open(result_filename, "r", encoding='utf-8') as f_out:
            result_message = f_out.read()
        bot.send_message(chat_id, f'Результата взлома: \n\n {result_message}')
        if os.path.exists(result_filename):
            os.remove(result_filename)
    except Exception as e:
        bot.reply_to(message, e.__str__())
    finally:
        bot.send_message(chat_id, 'Для того, чтобы начать работать сначала, нажмите /start',
                         reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(content_types=['document'])
def get_documents_messages(message):
    """
        Метод выполняетсяв в случае получения файла, неподпадающегося под более ранние фильтры.
    :param message:
        Содержит данные сообщения, откуда пришел вызов.
    """
    bot.send_message(message.chat.id, 'Я не знаю, что сейчас делать с этим файлом. Может начать сначала? '
                                      'Для этого введите /start')


@bot.message_handler(content_types=['photo'])
def get_documents_messages(message):
    """
        Метод выполняетсяв в случае получения сжатого изображения.
    :param message:
        Содержит данные сообщения, откуда пришел вызов.
    """
    bot.send_message(message.chat.id, 'Вы прислали сжатое фото, а надо без сжатия. Попробуйте еще раз, пожалуйста')


@bot.message_handler(content_types=['text'])
def text(message):
    """
        Метод выполняетсяв в случае получения сообщения с клавиатуры, неподпадающегося под более ранние фильтры.
    :param message:
        Содержит данные сообщения, откуда пришел вызов.
    """
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Я чего-то Вас не понимаю... Для получения справки введите /help')


def run_telebot():
    """
    Запуск бота.
    """
    bot.infinity_polling()

import os
import zlib

from cryptography.fernet import InvalidToken
import telebot
from telebot import types

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
code = None
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
def start(message):
    """
    Обработка команды '/start' в чате.
    Выдает в чат возможные режимы работы программы (шифрование, расшифрование, взлом шифра Цезаря).

    :param message:
    Сообщение '/start', по которому бот определяет id чата и имя пользователя.
    """
    global target, source, code, input_text, key, need_key_file, key_filename
    target = None
    source = None
    code = None
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

    :param message:
    :return:
    """
    chat_id = message.chat.id
    first_name = message.chat.first_name
    bot.send_message(message.from_user.id, "Напиши привет")


@bot.message_handler(content_types=['document'], func=lambda message: message.document.mime_type == 'image/bmp')
def get_documents_messages(message):
    """

    :param message:
    :return:
    """
    chat_id = message.chat.id
    if source == Constants.BMP:
        file_in_path = bot.get_file(message.document.file_id).file_path
        downloaded_file = bot.download_file(file_in_path)
        file_in_filename = write_bytes_to_file(downloaded_file, 'bmp')
        if target == Constants.DECODE:
            bmp = BMPChange(file_in_filename)
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


@bot.message_handler(content_types=['document'], func=lambda message: message.document.mime_type == 'image/jpeg')
def get_documents_messages(message):
    """

    :param message:
    :return:
    """
    chat_id = message.chat.id
    if source == Constants.JPG:
        file_in_path = bot.get_file(message.document.file_id).file_path
        downloaded_file = bot.download_file(file_in_path)
        file_in_filename = write_bytes_to_file(downloaded_file, 'jpg')
        if target == Constants.DECODE:
            jpg = JPGChange(file_in_filename)
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


@bot.message_handler(content_types=['document'],
                     func=lambda message: need_key_file and (message.document.mime_type == 'plain/text'))
def get_documents_messages(message):
    """

    :param message:
    :return:
    """
    global key_filename, need_key_file
    key_in_path = bot.get_file(message.document.file_id).file_path
    downloaded_key_file = bot.download_file(key_in_path)
    key_filename = write_bytes_to_file(downloaded_key_file, 'key')
    need_key_file = False
    steganography_start(message.chat.id, 'PNG')


@bot.message_handler(content_types=['document'], func=lambda message: message.document.mime_type == 'image/png')
def get_documents_messages(message):
    """

    :param message:
    :return:
    """
    chat_id = message.chat.id
    if source == Constants.PNG:
        file_in_path = bot.get_file(message.document.file_id).file_path
        downloaded_file = bot.download_file(file_in_path)
        file_in_filename = write_bytes_to_file(downloaded_file, 'png')
        if target == Constants.DECODE:
            png = PNGChange(file_in_filename, key_filename)
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


@bot.message_handler(content_types=['document'], func=lambda message: target == Constants.HACKING)
def get_documents_messages(message):
    """

    :param message:
    :return:
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


@bot.message_handler(content_types=['document'])
def get_documents_messages(message):
    """

    :param message:
    :return:
    """
    if target == Constants.HACKING:
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
        return
    if source == Constants.BMP:
        file_in = bot.get_file(message.document.file_id)
        print(file_in)


def get_input_message(chat_id):
    """

    :param chat_id:
    :return:
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_text = types.KeyboardButton(text='Ввести текстом...')
    keyboard_file = types.KeyboardButton(text='Прислать файл с текстом...')
    markup.add(keyboard_text, keyboard_file)
    bot.send_message(chat_id, 'Нужно сообщение для шифрования:', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Прислать файл с текстом...')
def text(message):
    """

    :param message:
    :return:
    """
    global input_text

    chat_id = message.chat.id
    if target == Constants.HACKING:
        bot.send_message(chat_id, 'OK! Оно и правильно, присылайте файл в формате txt, пожалуйста... '
                                  'Используйте для этого кнопку с изображением скрепочки)))')
        return
    # if target == Constants.ENCODE:
    #     if input_text is None:
    #         input_text = message.text
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     # keyboard_text = types.KeyboardButton(text='Ввести текстом...')
    #     keyboard_file = types.KeyboardButton(text='Прислать файл с текстом...')
    #     markup.add(keyboard_file)
    #     # bot.send_message(chat_id, 'Нужно сообщение для шифрования:', reply_markup=markup)
    #     bot.send_message(chat_id, 'Введите сообщение, которое надо зашифровать', reply_markup=markup)
    #     # get_input_message(chat_id)


@bot.message_handler(func=lambda message: need_key_file and message.text == 'Использовать ключ по умолчанию')
def text(message):
    """

    :param message:
    :return:
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
def text(message):
    """

    :param message:
    :return:
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


@bot.message_handler(content_types=['text'], func=lambda message: target is not None)
def text(message):
    """

    :param message:
    :return:
    """
    global input_text

    chat_id = message.chat.id
    if target == Constants.HACKING:
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

        return
    if message.text == 'Прислать файл с текстом...':
        bot.send_message(chat_id, 'Оно и правильно, присылайте файл в формате txt, пожалуйста...')
        return
    if target == Constants.ENCODE:
        if input_text is None:
            input_text = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # keyboard_text = types.KeyboardButton(text='Ввести текстом...')
        keyboard_file = types.KeyboardButton(text='Прислать файл с текстом...')
        markup.add(keyboard_file)
        # bot.send_message(chat_id, 'Нужно сообщение для шифрования:', reply_markup=markup)
        bot.send_message(chat_id, 'Введите сообщение, которое надо зашифровать', reply_markup=markup)
        # get_input_message(chat_id)


def sources_menu(chat_id, message_id, dist):
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f'Значит, будем {dist}...')
    inline_markup = types.InlineKeyboardMarkup(row_width=True)
    inline_keyboard_text = types.InlineKeyboardButton('текст', callback_data=Constants.TEXT)
    inline_keyboard_bmp = types.InlineKeyboardButton('bmp-изображение', callback_data=Constants.BMP)
    inline_keyboard_jpg = types.InlineKeyboardButton('jpg-изображение', callback_data=Constants.JPG)
    inline_keyboard_png = types.InlineKeyboardButton('png-изображение', callback_data=Constants.PNG)
    inline_markup.add(inline_keyboard_text, inline_keyboard_bmp, inline_keyboard_jpg, inline_keyboard_png)
    bot.send_message(chat_id, f"Что будем {dist}?", reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda call: call.data == Constants.ENCODE)
def callback_data(call):
    """

    :param call:
    :return:
    """
    global target
    chat_id = call.message.chat.id
    target = Constants.ENCODE
    sources_menu(chat_id, call.message.id, 'шифровать')


@bot.callback_query_handler(func=lambda call: call.data == Constants.DECODE)
def callback_data(call):
    """

    :param call:
    :return:
    """
    global target
    chat_id = call.message.chat.id
    target = Constants.DECODE
    sources_menu(chat_id, call.message.id, 'расшифровывать')


@bot.callback_query_handler(func=lambda call: call.data == Constants.HACKING)
def callback_data(call):
    """

    :param call:
    :return:
    """
    global target
    chat_id = call.message.chat.id
    target = Constants.HACKING
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.id, text='Значит, будем взламывать ' + '\U0001F609')
    input_message_menu(chat_id, 'взломать')


def input_message_menu(chat_id, message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_file = types.KeyboardButton(text='Прислать файл с текстом...')
    markup.add(keyboard_file)
    bot.send_message(chat_id, f'Введите сообщение, которое надо {message}', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == Constants.TEXT)
def callback_data(call):
    """

    :param call:
    :return:
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


def steganography_start(chat_id, file_type):
    if target == Constants.ENCODE:
        input_message_menu(chat_id, 'зашифровать')
    elif target == Constants.DECODE:
        bot.send_message(chat_id, f'Осталось только прислать мне {file_type}-файл для обработки '
                                  '(не забудьте снять галочку "сжать изображение")...')


@bot.callback_query_handler(func=lambda call: call.data == Constants.BMP)
def callback_data(call):
    """

    :param call:
    :return:
    """
    global source
    source = Constants.BMP
    chat_id = call.message.chat.id
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.id,
                          text='Вы выбрали режим работы с bmp-изображением...')
    steganography_start(chat_id, 'BMP')


@bot.callback_query_handler(func=lambda call: call.data == Constants.JPG)
def callback_data(call):
    """

    :param call:
    :return:
    """
    global source
    source = Constants.JPG
    chat_id = call.message.chat.id
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.id,
                          text='Вы выбрали режим работы с jpg-изображением...')
    steganography_start(chat_id, 'JPG')


@bot.callback_query_handler(func=lambda call: call.data == Constants.PNG)
def callback_data(call):
    """

    :param call:
    :return:
    """
    global source, need_key_file
    source = Constants.PNG
    need_key_file = True
    chat_id = call.message.chat.id

    bot.edit_message_text(chat_id=chat_id, message_id=call.message.id,
                          text='Вы выбрали режим работы с png-изображением...')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_default_key = types.KeyboardButton(text='Использовать ключ по умолчанию')
    keyboard_new_key = types.KeyboardButton(text='Сгенерировать новый ключ')
    markup.add(keyboard_default_key, keyboard_new_key)
    bot.send_message(chat_id, 'Введите ключ для обработки png-изображения вручную или пришлите файл с ключом...',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == Constants.CAESAR)
def callback_data(call):
    """

    :param call:
    :return:
    """
    global code
    chat_id = call.message.chat.id
    code = Constants.CAESAR
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.id, text='Шифр Цезаря, хороший выбор')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_file = types.KeyboardButton(text='Прислать файл с текстом...')
    markup.add(keyboard_file)
    bot.send_message(chat_id, 'Введите сообщение, которое надо зашифровать', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == Constants.VIJENER)
def callback_data(call):
    """

    :param call:
    :return:
    """
    global code
    chat_id = call.message.chat.id
    code = Constants.VIJENER


@bot.callback_query_handler(func=lambda call: call.data == Constants.VERNAM)
def callback_data(call):
    """

    :param call:
    :return:
    """
    global code
    chat_id = call.message.chat.id
    code = Constants.VERNAM


@bot.message_handler(content_types=['text'])
def text(message):
    """

    :param message:
    :return:
    """
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Я чего-то Вас не понимаю... Для получения справки введите /help')


def run_telebot():
    """
    Запуск бота.
    """
    bot.infinity_polling()

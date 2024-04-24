import os
import telebot
from telebot import types

from src.Hacking import CaesarHack
from src.MyTelebot.constants import Constants
from src.Tools import write_bytes_to_file, write_message_to_file

"""
Инициализация необходимых режимов
"""
target = None
source = None
input_text = None
code = None
key = None

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
    global target, source, code, input_text, key
    target = None
    source = None
    code = None
    input_text = None
    key = None
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

            src_message = write_bytes_to_file(downloaded_file)
            hack = CaesarHack()
            result_filename = hack.caesar_hacker(src_message)
            with open(result_filename, "rb") as f_out:
                result_message = f_out.read()
            bot.send_document(chat_id, result_message, visible_file_name=result_filename)
        except Exception as e:
            bot.reply_to(message, e.__str__())
        finally:
            if os.path.exists(result_filename):
                os.remove(result_filename)
            if os.path.exists(src_message):
                os.remove(src_message)
            bot.send_message(chat_id, 'Для того, чтобы начать работать сначала, нажмите /start',
                             reply_markup=types.ReplyKeyboardRemove())


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


@bot.message_handler(content_types=['text'])
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
            with open(result_filename, "r", encoding='utf-8') as f_out:
                result_message = f_out.read()
            bot.send_message(chat_id, f'Результата взлома: \n\n {result_message}')
        except Exception as e:
            bot.reply_to(message, e.__str__())
        finally:
            if os.path.exists(result_filename):
                os.remove(result_filename)
            if os.path.exists(src_message):
                os.remove(src_message)
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


@bot.callback_query_handler(func=lambda call: call.data == Constants.ENCODE)
def callback_data(call):
    """

    :param call:
    :return:
    """
    global target
    chat_id = call.message.chat.id
    target = Constants.ENCODE
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.id, text='Значит, будем шифровать...')
    inline_markup = types.InlineKeyboardMarkup(row_width=True)
    inline_keyboard_text = types.InlineKeyboardButton('текст', callback_data=Constants.TEXT)
    inline_keyboard_bmp = types.InlineKeyboardButton('bmp-изображение', callback_data=Constants.BMP)
    inline_keyboard_jpg = types.InlineKeyboardButton('jpg-изображение', callback_data=Constants.JPG)
    inline_keyboard_png = types.InlineKeyboardButton('png-изображение', callback_data=Constants.PNG)
    inline_markup.add(inline_keyboard_text, inline_keyboard_bmp, inline_keyboard_jpg, inline_keyboard_png)
    bot.send_message(chat_id, "Что будем шифровать?", reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda call: call.data == Constants.DECODE)
def callback_data(call):
    """

    :param call:
    :return:
    """
    global target
    chat_id = call.message.chat.id
    target = Constants.DECODE
    bot.send_message(chat_id, 'Значит, будем расшифровывать!')


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
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_file = types.KeyboardButton(text='Прислать файл с текстом...')
    markup.add(keyboard_file)
    bot.send_message(chat_id, 'Введите сообщение, которое надо зашифровать', reply_markup=markup)


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


@bot.callback_query_handler(func=lambda call: call.data == Constants.BMP)
def callback_data(call):
    """

    :param call:
    :return:
    """
    global source
    chat_id = call.message.chat.id
    source = Constants.BMP


@bot.callback_query_handler(func=lambda call: call.data == Constants.JPG)
def callback_data(call):
    """

    :param call:
    :return:
    """
    global source
    chat_id = call.message.chat.id
    source = Constants.JPG


@bot.callback_query_handler(func=lambda call: call.data == Constants.PNG)
def callback_data(call):
    """

    :param call:
    :return:
    """
    global source
    chat_id = call.message.chat.id
    source = Constants.PNG


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


@bot.callback_query_handler(func=lambda call: True)
def callback_data(call):
    """

    :param call:
    :return:
    """
    chat_id = call.message.chat.id
    bot.send_message(chat_id, 'Я чего-то Вас не понимаю... Для получения справки введите /help')


def run_telebot():
    """
    Запуск бота.
    """
    bot.infinity_polling()

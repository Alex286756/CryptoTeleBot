from stegano import exifHeader

from src.Abstract import AbstractImages


class JPGChange(AbstractImages):
    """
    Класс, реализующий шифрование текста в изображение JPG.

    Методы:
    ---------
    encoding(message_filename):
        Запуск процесса шифрования сообщения в файл изображения.
    decoding():
        Запуск процесса расшифрования сообщения из файла изображения.
    """

    def encoding(self, message_filename):
        """
        Осуществляет шифрование сообщения в файл с изображением.

        :param message_filename:
            Имя файла с сообщением.
        :return:
            Имя файла с изображением после обработки.
        """
        with open(message_filename, "r") as f:
            text = f.read()
        exifHeader.hide(self.in_filename, self.out_filename, text)
        return self.out_filename

    def decoding(self):
        """
        Осуществляет получение текстового сообщения из файла с изображением и сохраняет его в файл.

        :return:
            Имя файла с полученным сообщением.
        """
        result = exifHeader.reveal(self.in_filename).decode('utf-8')
        result_filename = self.get_decode_filename()
        with open(result_filename, "w") as f:
            f.write(result)
        return result_filename

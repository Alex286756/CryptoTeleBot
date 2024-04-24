from steganocryptopy.steganography import Steganography as StegoCript

from src.Abstract import AbstractImages


class PNGChange(AbstractImages):
    """
    Класс, реализующий шифрование текста в изображение PNG.

    Методы:
    ---------
    encoding(message_filename):
        Запуск процесса шифрования сообщения в файл изображения.
    decoding():
        Запуск процесса расшифрования сообщения из файла изображения.
    """

    def encoding(self, message_filename):
        """
        Осуществляет шифрование сообщения в файл с изображением (используется файл с ключом).

        :param message_filename:
            Имя файла с сообщением.
        :return:
            Имя файла с изображением после обработки.
        """
        secret = StegoCript.encrypt(self.key_filename, self.in_filename, message_filename)
        secret.save(self.out_filename)
        return self.out_filename

    def decoding(self):
        """
        Осуществляет получение текстового сообщения из файла с изображением и сохраняет его в файл.

        :return:
            Имя файла с полученным сообщением.
        """
        result = StegoCript.decrypt(self.key_filename, self.in_filename)
        result_filename = self.get_decode_filename()
        with open(result_filename, "w") as f:
            f.write(result)
        return result_filename

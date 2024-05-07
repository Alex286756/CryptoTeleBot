from src.Abstract import AbstractImages

from stegano import lsb


class BMPChange(AbstractImages):
    """
    Класс, реализующий шифрование текста в изображение BMP.

    Методы:
    ---------
    encoding(message_filename):
        Запуск процесса шифрования сообщения в файл изображения.
    decoding():
        Запуск процесса расшифрования сообщения из файла изображения.
    """

    def encoding(self, message_filename: str) -> str:
        """
        Осуществляет шифрование сообщения в файл с изображением.

        :param message_filename:
            Имя файла с сообщением.
        :return:
            Имя файла с изображением после обработки.
        """
        with open(message_filename, "r", encoding='utf-8') as f:
            text = f.read()
        secret = lsb.hide(self.in_filename, text, encoding="UTF-8")
        secret.save(self.out_filename)
        return self.out_filename

    def decoding(self) -> str:
        """
        Осуществляет получение текстового сообщения из файла с изображением и сохраняет его в файл.

        :return:
            Имя файла с полученным сообщением.
        """
        result = lsb.reveal(self.in_filename, encoding="UTF-8")
        result_filename = self.get_decode_filename()
        with open(result_filename, "w", encoding="UTF-8") as f:
            f.write(result)
        return result_filename

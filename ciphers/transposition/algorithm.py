import string

from ciphers.abc import AbstractCipher


class TranspositionCipher(AbstractCipher):
    """
    Класс, представляющий шифр перестановки.

    Параметры:
    - block_size: Размер блока для перестановки (по умолчанию 5).
    - padding_str: Строка-заполнитель для дополнения текста (по умолчанию "о").
    """

    def __init__(self, block_size: int = 5, padding_str: str = "о"):
        self.__block_size = block_size
        self.__padding_str = padding_str

    def __repr__(self):
        """
        Возвращает строку с описанием объекта.

        Пример:
        "TranspositionCipher(block_size=5, padding_str=о)"
        """
        return (
            f"TranspositionCipher"
            f"(block_size={self.__block_size}, "
            f"padding_str={self.__padding_str})"
        )

    @property
    def block_size(self):
        """
        Свойство для получения размера блока.
        """
        return self.__block_size

    @staticmethod
    def prepare_text(text: str):
        """
        Подготавливает текст для обработки:
        - Приводит к нижнему регистру.
        - Удаляет пробелы.
        - Удаляет знаки пунктуации.

        Возвращает подготовленный текст.
        """
        result = (
            text.lower()
            .replace(" ", "")
            .translate(str.maketrans("", "", string.punctuation))
        )
        return result

    def __pad_text(self, text: str):
        """
        Дополняет текст строкой-заполнителем до размера блока.

        Возвращает дополненный текст.
        """
        remainder = len(text) % self.__block_size
        if remainder != 0:
            text += self.__padding_str * (self.__block_size - remainder)
        return text

    def __apply_transposition(self, text):
        """
        Применяет шифр перестановки к тексту:
        - Подготавливает текст.
        - Дополняет текст.
        - Выполняет перестановку блоков.

        Возвращает зашифрованный (или расшифрованный) текст.
        """
        text = self.prepare_text(text)
        text = self.__pad_text(text)
        result = []
        for i in range(0, len(text), self.__block_size):
            block = text[i: i + self.__block_size]
            result.insert(-i, block[::-1])
        result_text = " ".join(result)
        return result_text

    def encrypt(self, plaintext):
        """
        Шифрует переданный текст методом перестановки.

        Возвращает зашифрованный текст.
        """
        return self.__apply_transposition(plaintext)

    def decrypt(self, ciphertext):
        """
        Расшифровывает переданный зашифрованный текст методом перестановки.

        Возвращает расшифрованный текст.
        """
        plaintext = self.__apply_transposition(ciphertext)
        plaintext = plaintext.rstrip(self.__padding_str)
        return plaintext

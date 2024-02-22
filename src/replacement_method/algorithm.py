import pprint
import string
from typing import Literal

from loguru import logger


class TrithemiusCipherException(Exception):
    pass


class TrithemiusCipher:
    ALPHABETS = {
        "ru": "абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
        "en": "abcdefghijklmnopqrstuvwxyz",
    }

    PUNCTUATION: str = string.punctuation + " " + "’"
    NUMBERS: str = "0123456789"

    def __init__(
        self,
        lang: Literal["ru", "en"] | str = "ru",
        keyword: str = "",
        shift: int = 1,
        use_punctiation: bool = True,
        use_numbers: bool = True,
    ):
        """
        :param lang: Literal["ru", "en"] | str: Язык алфавита (русский или английский).
        :param keyword: str: Ключевое слово для шифрования.
        :param shift: int: Сдвиг для шифрования.
        :param use_punctiation: bool: Флаг использования знаков препинания.
        :param use_numbers: bool: Флаг использования цифр.
        """
        self.lang = lang

        self.__keyword = keyword.lower()
        assert (
            self.is_symbols_in_alphabet(
                text=self.__keyword, alphabet=self.ALPHABETS[self.lang]
            )[0]
            is True
        ), f"symbol not exist in {self.lang} alphabet"

        self.__shift = shift
        self.__use_punctiation = use_punctiation
        self.__use_numbers = use_numbers

        self.__row_length = 6
        self.__unique_keyword = "".join(
            sorted(set(self.__keyword), key=self.__keyword.index)
        )
        self.__remaining_chars = "".join(
            sorted(set(self.ALPHABETS[self.lang]) - set(self.__unique_keyword))
        )

        self.__alphabet = self.__unique_keyword + self.__remaining_chars

        if use_punctiation:
            self.__alphabet += self.PUNCTUATION
        if use_numbers:
            self.__alphabet += self.NUMBERS

        self.trithemius_alphabet_table = self.__generate_trithemius_table()
        if (
            len(self.trithemius_alphabet_table) > 0
            and len(self.trithemius_alphabet_table[-1]) < self.__row_length
        ):
            self.trithemius_alphabet_table[-1].extend(
                [
                    " "
                    for _ in range(
                        self.__row_length - len(self.trithemius_alphabet_table[-1])
                    )
                ]
            )
        trithemius_alphabet_table_string = pprint.pformat(
            self.trithemius_alphabet_table, indent=2
        )
        logger.info(f"trithemius_alphabet_table:\n{trithemius_alphabet_table_string}")
        assert (
            0 <= self.__shift < len(self.trithemius_alphabet_table)
        ), f"shift must be ge 0 and lt {len(self.trithemius_alphabet_table)}"

    def __repr__(self):
        return (
            f"TrithemiusCipher"
            f"(lang={self.lang}, "
            f"keyword={self.__keyword}, "
            f"shift={self.__shift}, "
            f"use_punctiation={self.__use_punctiation}, "
            f"use_numbers={self.__use_numbers})"
        )

    @staticmethod
    def is_symbols_in_alphabet(
        text: str | list[str], alphabet: str | list[str]
    ) -> tuple[bool, str] | tuple[bool]:
        """
        Проверяет, принадлежат ли символы текста алфавиту.

        :param text: str | list[str]: Текст или список символов для проверки.
        :param alphabet: str | list[str]: Алфавит, в котором проверяются символы.
        """
        for symbol in text:
            if symbol.lower() not in alphabet:
                return False, symbol
        return (True,)

    def __generate_trithemius_table(self):
        """
        Генерирует таблицу Тритемия на основе алфавита.

        :return: list[list[str]]
        """
        return [
            list(self.__alphabet[i : i + self.__row_length])
            for i in range(0, len(self.__alphabet), self.__row_length)
        ]

    def __find_position(self, char):
        """
        Находит позицию символа в таблице Тритемия.

        :param char: str: Символ для поиска.

        :return: tuple[int, int] | None: Кортеж (row, col) - координаты символа в таблице.

        Если символ не найден, возвращается None.
        """
        for row, row_chars in enumerate(self.trithemius_alphabet_table):
            if char in row_chars:
                col = row_chars.index(char)
                return row, col
        return None

    def __update_position(self, row, col, shift):
        """
        Обновляет позицию символа в таблице Тритемия с учетом сдвига.

        :param row: int: Начальная строка символа.
        :param col: int: Начальный столбец символа.
        :param shift: int: Сдвиг.

        :return: tuple[int, int]: Кортеж (new_row, new_col) - новые координаты символа.
        """
        return (row + shift) % len(self.trithemius_alphabet_table), col

    def __process_message(
        self, message: str, shift: int, action: Literal["encrypt", "decrypt"]
    ):
        """
        Обрабатывает сообщение для шифрования или дешифрования.

        :param message: str: Сообщение для обработки.
        :param shift: int: Сдвиг для шифрования или дешифрования.

        :return: str: Обработанное сообщение.
        """
        message = message.lower().replace("\n", "").replace("\t", "")
        processed_text = ""
        for char in message:
            if char == " ":
                processed_text += char
                continue
            row, col = self.__find_position(char)
            new_row, new_col = self.__update_position(row, col, shift)
            processed_text += self.trithemius_alphabet_table[new_row][new_col]
            logger.debug(
                f"{action} '{char}'[{row}, {col}] -> '{self.trithemius_alphabet_table[new_row][new_col]}' [{new_row}, {new_col}]"
            )
        return processed_text

    def encrypt(self, plaintext):
        """
        Шифрует переданный текст методом Тритемия.

        :param plaintext: str: Текст для шифрования.

        :return: str: Зашифрованный текст.
        """
        check_result = self.is_symbols_in_alphabet(
            text=plaintext, alphabet=self.__alphabet
        )
        if not check_result[0]:
            raise Exception(
                f"symbol '{check_result[1]}' not exist in {self.lang} alphabet"
            )
        return self.__process_message(plaintext, self.__shift, "encrypt")

    def decrypt(self, ciphertext):
        """
        Дешифрует переданный зашифрованный текст методом Тритемия.

        :param ciphertext: str: Зашифрованный текст.

        :return: str: Расшифрованный текст.
        """
        return self.__process_message(ciphertext, -self.__shift, "decrypt")

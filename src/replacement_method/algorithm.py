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
        self.lang = lang

        self.__keyword = keyword.lower().replace(" ", "")
        assert self.is_symbols_in_alphabet(
            text=self.__keyword, alphabet=self.ALPHABETS[self.lang]
        ), f"symbol not exist in {self.lang} alphabet"

        self.__shift = shift
        self.__row_length = 6

        self.__unique_keyword = "".join(
            sorted(set(self.__keyword), key=self.__keyword.index)
        )
        self.__remaining_chars = "".join(
            sorted(set(self.ALPHABETS[self.lang]) - set(self.__unique_keyword))
        )

        self.__alphabet = (
            self.__unique_keyword + self.__remaining_chars + self.PUNCTUATION
            if use_punctiation
            else "" + self.NUMBERS if use_numbers else ""
        )

        self.trithemius_alphabet_table = self.__generate_trithemius_table()

        if len(self.trithemius_alphabet_table[-1]) < self.__row_length:
            self.trithemius_alphabet_table[-1].extend(
                [
                    " "
                    for _ in range(
                    self.__row_length - len(self.trithemius_alphabet_table[-1])
                )
                ]
            )

        assert (
            0 <= self.__shift < len(self.trithemius_alphabet_table)
        ), f"shift must be ge 0 and lt {len(self.trithemius_alphabet_table)}"

    def __repr__(self):
        return (
            f"TrithemiusCipher"
            f"(lang={self.lang}, "
            f"keyword={self.__keyword}, "
            f"shift={self.__shift})"
        )

    @staticmethod
    def is_symbols_in_alphabet(
        text: str | list[str], alphabet: str | list[str]
    ) -> tuple[bool, str] | tuple[bool]:
        for symbol in text:
            if symbol.lower() not in alphabet:
                return False, symbol
        return (True,)

    def __generate_trithemius_table(self):
        return [
            list(self.__alphabet[i: i + self.__row_length])
            for i in range(0, len(self.__alphabet), self.__row_length)
        ]

    def __find_position(self, char):
        for row, row_chars in enumerate(self.trithemius_alphabet_table):
            if char in row_chars:
                col = row_chars.index(char)
                return row, col
        return None

    def __update_position(self, row, col, shift):
        return (row + shift) % len(self.trithemius_alphabet_table), col

    def __process_message(self, message: str, shift: int):
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
                f"'{char}'[{row}, {col}] -> '{self.trithemius_alphabet_table[new_row][new_col]}' [{new_row}, {new_col}]"
            )
        return processed_text

    def encrypt(self, plaintext):
        check_result = self.is_symbols_in_alphabet(text=plaintext, alphabet=self.__alphabet)
        if not check_result[0]:
            raise Exception(f"symbol '{check_result[1]}' not exist in {self.lang} alphabet")
        return self.__process_message(plaintext, self.__shift)

    def decrypt(self, ciphertext):
        return self.__process_message(ciphertext, -self.__shift)

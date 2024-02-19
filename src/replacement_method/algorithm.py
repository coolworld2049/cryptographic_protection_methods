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
        *,
        keyword: str = "",
        shift: int = 1,
    ):
        self.lang = lang
        self.alphabet = self.ALPHABETS[self.lang]

        self.keyword = keyword.lower().replace(" ", "")
        self.shift = shift

        self.__shape = 6
        self.__unique_keyword = "".join(
            sorted(set(self.keyword), key=self.keyword.index)
        )
        self.__remaining_chars = "".join(
            sorted(set(self.alphabet) - set(self.__unique_keyword))
        )
        self.trithemius_alphabet = (
            self.__unique_keyword
            + self.__remaining_chars
            + self.PUNCTUATION
            + self.NUMBERS
        )

        self.table = self.__generate_table()

        if len(self.table[-1]) < self.__shape:
            self.table[-1].extend(
                [" " for _ in range(self.__shape - len(self.table[-1]))]
            )

        assert (
            0 <= self.shift < len(self.table)
        ), f"shift must be ge 0 and lt {len(self.table)}"

    def __repr__(self):
        return (
            f"TrithemiusCipher"
            f"(lang={self.lang}, "
            f"keyword={self.keyword}, "
            f"shift={self.shift})"
        )

    def __generate_table(self):
        return [
            list(self.trithemius_alphabet[i : i + self.__shape])
            for i in range(0, len(self.trithemius_alphabet), self.__shape)
        ]

    def __find_position(self, char):
        for row, row_chars in enumerate(self.table):
            if char in row_chars:
                col = row_chars.index(char)
                return row, col
        return None

    def __update_position(self, row, col, shift):
        return (row + shift) % len(self.table), col

    def __process_message(self, message: str, shift: int):
        message = message.lower().replace("\n", "").replace("\t", "")
        processed_text = ""
        for char in message:
            if char == " ":
                processed_text += char
                continue
            row, col = self.__find_position(char)
            new_row, new_col = self.__update_position(row, col, shift)
            processed_text += self.table[new_row][new_col]
            logger.debug(
                f"'{char}'[{row}, {col}] -> '{self.table[new_row][new_col]}' [{new_row}, {new_col}]"
            )
        return processed_text

    def is_in_trithemius_alphabet(self, text: str):
        for i, char in enumerate(text):
            if char.lower() not in self.trithemius_alphabet:
                raise TrithemiusCipherException(
                    f"symbol '{char}' at index {i} not exist in {self.lang} alphabet"
                )

    def encrypt(self, plaintext):
        self.is_in_trithemius_alphabet(plaintext)
        return self.__process_message(plaintext, self.shift)

    def decrypt(self, ciphertext):
        return self.__process_message(ciphertext, -self.shift)

import string

from loguru import logger


class TrithemiusCipherException(Exception):
    pass


class TrithemiusCipher:
    def __init__(self, alphabet: str, keyword: str, shift: int = 1):
        self._alphabet = alphabet.lower()
        self._keyword = keyword.lower().replace(" ", "")
        self._shift = shift

        self._unique_keyword = "".join(
            sorted(set(self._keyword), key=self._keyword.index)
        )
        self._remaining_chars = "".join(
            sorted(set(self._alphabet) - set(self._unique_keyword))
        )
        self._square_string = (
            self._unique_keyword + self._remaining_chars + string.punctuation + " "
        )

        self.trithemius_table = self.__generate_table()
        assert (
            0 <= self._shift <= len(self.trithemius_table)
        ), f"shift must be ge 0 and le {len(self.trithemius_table)}"

    def __repr__(self):
        return (
            f"TrithemiusCipher"
            f"(alphabet={self._alphabet}, "
            f"keyword={self._keyword}, "
            f"shift={self._shift})"
        )

    def __generate_table(self):
        return [
            list(self._square_string[i : i + 6])
            for i in range(0, len(self._square_string), 6)
        ]

    def __find_position(self, char):
        for row, row_chars in enumerate(self.trithemius_table):
            if char in row_chars:
                col = row_chars.index(char)
                return row, col
        return None

    def __update_position(self, row, col, shift):
        return (row + shift) % len(self.trithemius_table), col

    def __process_message(self, message: str, shift: int):
        message = message.lower().replace("\n", "").replace("\t", "")
        processed_text = ""
        for char in message:
            if char == " ":
                processed_text += char
                continue
            row, col = self.__find_position(char)
            new_row, new_col = self.__update_position(row, col, shift)
            processed_text += self.trithemius_table[new_row][new_col]
            logger.debug(
                f"'{char}'[{row}, {col}] -> '{self.trithemius_table[new_row][new_col]}' [{new_row}, {new_col}]"
            )
        return processed_text

    def encrypt(self, plaintext):
        is_message_in__square_string = list(
            map(lambda c: c.lower() in self._square_string, list(plaintext))
        )
        if not all(is_message_in__square_string):
            raise TrithemiusCipherException(
                "Encrypt: Input symbol is not part of the alphabet"
            )
        return self.__process_message(plaintext, self._shift)

    def decrypt(self, ciphertext):
        return self.__process_message(ciphertext, -self._shift)

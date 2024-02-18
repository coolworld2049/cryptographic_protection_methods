import string

import flet as ft
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


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.window_width = 600
    page.title = "Trithemius Cipher"
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN

    alphabet_default = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    keyword_defualt = "ключ"
    shift_defualt = 1
    page.trithemius_cipher = TrithemiusCipher(
        alphabet=alphabet_default, keyword=keyword_defualt, shift=1
    )
    trithemius_cipher_error_t = ft.Text()
    trithemius_cipher_error_dlg = ft.AlertDialog(
        title=trithemius_cipher_error_t, bgcolor=ft.colors.ON_ERROR
    )

    def update_trithemius_cipher_instance(e):
        page.trithemius_cipher = TrithemiusCipher(
            alphabet=alphabet_tb.value,
            keyword=keyword_tb.value,
            shift=int(shift_tb.value),
        )
        logger.info(f"Initialize {page.trithemius_cipher}")

    def on_change_message(e):
        update_trithemius_cipher_instance(e)
        try:
            encrypted_tb.value = page.trithemius_cipher.encrypt(message_tb.value)
            decrypted_tb.value = page.trithemius_cipher.decrypt(encrypted_tb.value)
        except TrithemiusCipherException as e:
            logger.error(e)
            trithemius_cipher_error_t.value = " ".join(e.args)
            page.dialog = trithemius_cipher_error_dlg
            trithemius_cipher_error_dlg.open = True
        page.update()

    alphabet_tb = ft.TextField(
        label="alphabet", value=alphabet_default, on_change=on_change_message
    )
    keyword_tb = ft.TextField(
        label="key", value=keyword_defualt, on_change=on_change_message
    )
    shift_tb = ft.TextField(label="shift", value=str(shift_defualt))

    message_tb = ft.TextField(
        label="Message",
        multiline=True,
        hint_text="Enter message to encrypt",
        on_change=on_change_message,
    )
    encrypted_tb = ft.TextField(
        label="Encrypted",
        read_only=True,
        multiline=True,
    )
    decrypted_tb = ft.TextField(
        label="Decrypted",
        read_only=True,
        multiline=True,
    )

    def shift_slider_changed(e):
        shift_tb.value = e.control.value
        on_change_message(e)
        page.update()

    page.add(
        alphabet_tb,
        keyword_tb,
        shift_tb,
        ft.Slider(
            min=0,
            value=1,
            max=len(page.trithemius_cipher.trithemius_table),
            divisions=len(page.trithemius_cipher.trithemius_table),
            on_change=shift_slider_changed,
        ),
        message_tb,
        encrypted_tb,
        decrypted_tb,
    )


if __name__ == "__main__":
    ft.app(target=main)

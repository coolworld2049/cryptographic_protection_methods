import flet as ft
from loguru import logger

from algorithm import (
    TrithemiusCipher,
    TrithemiusCipherException,
)


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

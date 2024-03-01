import typing

import flet as ft
from loguru import logger

from cipher.substitution.algorithm import TrisemusSubstitutionCipher


def substitution_cipher_controls(
    page: ft.Page,
) -> list[typing.Type["ft.Control"]]:
    page.trisemus_cipher = TrisemusSubstitutionCipher()
    trisemus_cipher_error_t = ft.Text()
    trisemus_cipher_error_dlg = ft.AlertDialog(
        title=trisemus_cipher_error_t, bgcolor=ft.colors.ON_ERROR
    )

    def on_change_message(e):
        try:
            page.Trisemus_cipher = TrisemusSubstitutionCipher(
                lang=language_dd.value,
                keyword=keyword_tb.value,
                shift=int(shift_tb.value),
                use_punctiation=use_punctiation_c.value,
                use_numbers=use_numbers_c.value,
            )
            logger.info(f"Initialize {page.Trisemus_cipher}")
            encrypted_tb.value = page.Trisemus_cipher.encrypt(message_tb.value)
            decrypted_tb.value = page.Trisemus_cipher.decrypt(encrypted_tb.value)
        except Exception as e:
            logger.error(e)
            trisemus_cipher_error_t.value = "\n".join(e.args)
            page.dialog = trisemus_cipher_error_dlg
            trisemus_cipher_error_dlg.open = True
        page.update()

    def on_change_language_dd(e):
        language_dd.value = e.control.value
        keyword_tb.value = None
        shift_tb.value = 1
        shift_slider.value = 1
        message_tb.value = None
        encrypted_tb.value = None
        decrypted_tb.value = None
        page.update()
        on_change_message(e)

    language_dd = ft.Dropdown(
        width=100,
        options=[
            ft.dropdown.Option("ru"),
            ft.dropdown.Option("en"),
        ],
        value=page.trisemus_cipher.lang,
        on_change=on_change_language_dd,
    )
    use_punctiation_c = ft.Checkbox(
        label="Punctiation", value=True, on_change=on_change_message
    )
    use_numbers_c = ft.Checkbox(
        label="Numbers", value=True, on_change=on_change_message
    )
    keyword_tb = ft.TextField(label="key", on_change=on_change_message)
    shift_tb = ft.TextField(label="shift", value=str(1))

    def shift_slider_changed(e):
        shift_tb.value = e.control.value
        on_change_message(e)
        page.update()

    shift_slider = ft.Slider(
        min=0,
        value=1,
        max=len(page.trisemus_cipher.Trisemus_alphabet_table) - 2,
        divisions=len(page.trisemus_cipher.Trisemus_alphabet_table) - 2,
        on_change=shift_slider_changed,
    )
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

    controls = [
        ft.Row(
            controls=[
                ft.Text("Language"),
                language_dd,
            ]
        ),
        keyword_tb,
        shift_tb,
        shift_slider,
        ft.Row(
            controls=[
                use_punctiation_c,
                use_numbers_c,
            ]
        ),
        message_tb,
        encrypted_tb,
        decrypted_tb,
    ]
    return controls

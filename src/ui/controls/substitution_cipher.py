import typing

import flet as ft
from loguru import logger

from src.cipher.substitution.algorithm import TrisemusSubstitutionCipher


def substitution_cipher_controls(
    page: ft.Page,
) -> list[typing.Type["ft.Control"]]:
    page.cipher = TrisemusSubstitutionCipher(keyword="республика")
    error_t = ft.Text()
    error_dlg = ft.AlertDialog(title=error_t, bgcolor=ft.colors.ON_ERROR)

    def on_change(e):
        try:
            page.cipher = TrisemusSubstitutionCipher(
                lang=language_dd.value,
                keyword=keyword_tb.value,
                shift=int(shift_slider.value),
                use_punctiation=use_punctiation_c.value,
                use_numbers=use_numbers_c.value,
            )
            shift_slider.max = len(page.cipher.trisemus_alphabet_table) - 2
            shift_slider.divisions = shift_slider.max
            logger.info(page.cipher)
            encrypted_tb.value = page.cipher.encrypt(message_tb.value)
            decrypted_tb.value = page.cipher.decrypt(encrypted_tb.value)
        except Exception as e:
            logger.error(e)
            error_t.value = "\n".join(e.args)
            page.dialog = error_dlg
            error_dlg.open = True
        page.update()

    def on_change_language_dd(e):
        language_dd.value = e.control.value
        keyword_tb.value = None
        shift_slider.value = 1
        message_tb.value = None
        encrypted_tb.value = None
        decrypted_tb.value = None
        page.update()
        on_change(e)

    language_dd = ft.Dropdown(
        width=100,
        options=[
            ft.dropdown.Option("ru"),
            ft.dropdown.Option("en"),
        ],
        value=page.cipher.lang,
        on_change=on_change_language_dd,
    )
    use_punctiation_c = ft.Checkbox(
        label="Punctiation", value=True, on_change=on_change
    )
    use_numbers_c = ft.Checkbox(label="Numbers", value=True, on_change=on_change)
    keyword_tb = ft.TextField(
        label="key", value=page.cipher.keyword, on_change=on_change
    )
    shift_slider = ft.Slider(
        min=0,
        value=1,
        label="shift: {value}",
        max=len(page.cipher.trisemus_alphabet_table) - 2,
        divisions=len(page.cipher.trisemus_alphabet_table) - 2,
        on_change=on_change,
    )
    message_tb = ft.TextField(
        label="Message",
        multiline=True,
        hint_text="Enter message to encrypt",
        on_change=on_change,
    )
    message_tb.value = "слива"
    encrypted_tb = ft.TextField(
        label="Encrypted",
        read_only=True,
        multiline=True,
    )
    encrypted_tb.value = page.cipher.encrypt(message_tb.value)
    decrypted_tb = ft.TextField(
        label="Decrypted",
        read_only=True,
        multiline=True,
    )
    decrypted_tb.value = page.cipher.decrypt(encrypted_tb.value)
    controls = [
        ft.Row(
            controls=[
                ft.Text("Language"),
                language_dd,
            ]
        ),
        keyword_tb,
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

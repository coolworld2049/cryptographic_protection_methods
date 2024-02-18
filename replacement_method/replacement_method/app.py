import flet as ft
from loguru import logger

from replacement_method.replacement_method.algorithm import (
    TrithemiusCipher,
    TrithemiusCipherException,
)


def app_bar(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 600
    page.window_height = 800

    def theme_changed(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_switch.thumb_icon = ft.icons.DARK_MODE
        elif page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_switch.thumb_icon = ft.icons.SUNNY
        page.update()

    theme_switch = ft.Switch(thumb_icon=ft.icons.SUNNY, on_change=theme_changed)

    page.appbar = ft.AppBar(
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            theme_switch,
        ],
    )


def main(page: ft.Page):
    app_bar(page)

    page.title = "Trithemius Cipher"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    alphabet_default = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    keyword_defualt = "секретный ключ"
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
            alphabet=alphabet_tb.value, keyword=key_tb.value, shift=int(shift_tb.value)
        )
        logger.info(page.trithemius_cipher)

    def message_on_focus(e):
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
        label="Alphabet", value=alphabet_default, on_change=message_on_focus
    )
    key_tb = ft.TextField(
        label="Key", value=keyword_defualt, on_change=message_on_focus
    )
    shift_tb = ft.TextField(label="Shift", value=str(shift_defualt))

    message_tb = ft.TextField(
        label="Message",
        multiline=True,
        text_size=20,
        on_change=message_on_focus,
    )
    encrypted_tb = ft.TextField(
        label="Encrypted",
        read_only=True,
        multiline=True,
        text_size=20,
    )
    decrypted_tb = ft.TextField(
        label="Decrypted",
        read_only=True,
        multiline=True,
        text_size=20,
    )

    def shift_slider_changed(e):
        shift_tb.value = e.control.value
        message_on_focus(e)
        page.update()

    page.add(
        alphabet_tb,
        key_tb,
        shift_tb,
        ft.Slider(
            min=0,
            value=1,
            max=len(page.trithemius_cipher.trithemius_table),
            divisions=len(page.trithemius_cipher.trithemius_table),
            on_change=shift_slider_changed,
        ),
        ft.Divider(),
        message_tb,
        encrypted_tb,
        decrypted_tb,
    )


ft.app(target=main)

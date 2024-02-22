import flet as ft
from loguru import logger

from replacement_method.algorithm import TrithemiusCipher


def main(page: ft.Page):
    page.title = "Trithemius Cipher"
    page.window_width = 800
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
    page.trithemius_cipher = TrithemiusCipher()
    trithemius_cipher_error_t = ft.Text()
    trithemius_cipher_error_dlg = ft.AlertDialog(
        title=trithemius_cipher_error_t, bgcolor=ft.colors.ON_ERROR
    )
    page.window_center()

    def on_change_message(e):
        try:
            page.trithemius_cipher = TrithemiusCipher(
                lang=language_dd.value,
                keyword=keyword_tb.value,
                shift=int(shift_tb.value),
                use_punctiation=use_punctiation_c.value,
                use_numbers=use_numbers_c.value,
            )
            logger.info(f"Initialize {page.trithemius_cipher}")
            encrypted_tb.value = page.trithemius_cipher.encrypt(message_tb.value)
            decrypted_tb.value = page.trithemius_cipher.decrypt(encrypted_tb.value)
        except Exception as e:
            logger.error(e)
            trithemius_cipher_error_t.value = "\n".join(e.args)
            page.dialog = trithemius_cipher_error_dlg
            trithemius_cipher_error_dlg.open = True
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
        value=page.trithemius_cipher.lang,
        on_change=on_change_language_dd,
    )
    use_punctiation_c = ft.Checkbox(label="Punctiation", value=True)
    use_numbers_c = ft.Checkbox(label="Numbers", value=True)
    keyword_tb = ft.TextField(label="key", on_change=on_change_message)
    shift_tb = ft.TextField(label="shift", value=str(1))

    def shift_slider_changed(e):
        shift_tb.value = e.control.value
        on_change_message(e)
        page.update()

    shift_slider = ft.Slider(
        min=0,
        value=1,
        max=len(page.trithemius_cipher.trithemius_alphabet_table) - 2,
        divisions=len(page.trithemius_cipher.trithemius_alphabet_table) - 2,
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

    page.add(
        ft.Row(
            controls=[
                ft.Text("Language"),
                language_dd,
                use_punctiation_c,
                use_numbers_c,
            ]
        ),
        keyword_tb,
        shift_tb,
        shift_slider,
        message_tb,
        encrypted_tb,
        decrypted_tb,
    )


if __name__ == "__main__":
    ft.app(main)

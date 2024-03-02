import typing

import flet as ft
from loguru import logger

from ciphers.substitution.algorithm import TrisemusSubstitutionCipher
from ciphers.transposition.algorithm import TranspositionCipher


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


def transposition_cipher_controls(
    page: ft.Page,
) -> list[typing.Type["ft.Control"]]:
    page.cipher = TranspositionCipher()

    def on_change(e):
        page.cipher = TranspositionCipher(
            block_size=int(block_size_slider.value),
        )
        logger.info(page.cipher)
        try:
            encrypted_tx.value = page.cipher.encrypt(message_tx.value)
            decrypted_tx.value = page.cipher.decrypt(encrypted_tx.value)
        except Exception as e:
            logger.error(e)
        page.update()

    block_size_slider = ft.Slider(
        min=2,
        value=5,
        max=10,
        divisions=10,
        label="block size: {value}",
        on_change=on_change,
    )
    message_tx = ft.TextField(
        label="Message",
        multiline=True,
        hint_text="Enter message to encrypt",
        on_change=on_change,
    )
    message_tx.value = "ПУСТЬ БУДЕТ ТАК, КАК МЫ ХОТЕЛИ"
    encrypted_tx = ft.TextField(
        label="Encrypted",
        read_only=True,
        multiline=True,
    )
    encrypted_tx.value = page.cipher.encrypt(message_tx.value)
    decrypted_tx = ft.TextField(
        label="Decrypted",
        read_only=True,
        multiline=True,
    )
    decrypted_tx.value = page.cipher.encrypt(encrypted_tx.value)

    controls = [
        block_size_slider,
        message_tx,
        encrypted_tx,
        decrypted_tx,
    ]
    return controls


def main(page: ft.Page):
    page.title = "Cryptographic algorithms"
    page.window_width = 600
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
    page.window_center()

    def route_change(route):
        page.views.clear()
        c1 = ft.Container(
            content=ft.Column(
                [
                    ft.Image(
                        "./assets/gravity_falls.png",
                        width=150,
                        height=150,
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    ft.Text("Substitution  Cipher", size=20),
                ],
            ),
            margin=10,
            padding=10,
            alignment=ft.alignment.center,
            width=150,
            height=150,
            border_radius=10,
            ink=True,
            on_click=lambda _: page.go("/substitution_cipher"),
        )
        c2 = ft.Container(
            content=ft.Column(
                [
                    ft.Image(
                        "./assets/scytale.png",
                        width=150,
                        height=150,
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    ft.Text("Transposition Cipher", size=20),
                ],
            ),
            margin=10,
            padding=10,
            alignment=ft.alignment.center,
            width=150,
            height=150,
            border_radius=10,
            ink=True,
            on_click=lambda _: page.go("/transposition_cipher"),
        )
        c3 = ft.Container(
            content=ft.Column(
                [
                    ft.Image(
                        "./assets/gamma.png",
                        width=150,
                        height=150,
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    ft.Text("Gamma  Cipher", size=20),
                ],
            ),
            margin=10,
            padding=10,
            alignment=ft.alignment.center,
            width=150,
            height=150,
            border_radius=10,
            ink=True,
            on_click=lambda _: page.go("/gamma_cipher"),
        )
        page.views.append(
            ft.View(
                "/",
                [
                    ft.Row(
                        controls=[c1, c2, c3],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                ],
            )
        )
        if page.route == "/substitution_cipher":
            page.views.append(
                ft.View(
                    "/substitution_cipher",
                    controls=[
                        ft.AppBar(
                            title=c1.content.controls[1],
                            bgcolor=ft.colors.SURFACE_VARIANT,
                        ),
                        *substitution_cipher_controls(page),
                    ],
                )
            )
        elif page.route == "/transposition_cipher":
            page.views.append(
                ft.View(
                    "/transposition_cipher",
                    controls=[
                        ft.AppBar(
                            title=c2.content.controls[1],
                            bgcolor=ft.colors.SURFACE_VARIANT,
                        ),
                        *transposition_cipher_controls(page),
                    ],
                )
            )
        elif page.route == "/gamma_cipher":
            page.views.append(
                ft.View(
                    "/gamma_cipher",
                    controls=[
                        ft.AppBar(
                            title=c3.content.controls[1],
                            bgcolor=ft.colors.SURFACE_VARIANT,
                        ),
                    ],
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.FLET_APP)

import typing

import flet as ft
from loguru import logger

from ciphers.block import gost_34_13_2015
from ciphers.block.gost_34_13_2015 import GOST_34_13_2015_GammaOutputFeedback
from ciphers.substitution.algorithm import TrisemusSubstitutionCipher
from ciphers.transposition.algorithm import TranspositionCipher


def substitution_cipher_controls(
    page: ft.Page,
) -> list[typing.Type["ft.Control"]]:
    page.cipher = TrisemusSubstitutionCipher(keyword="республика")
    error_t = ft.Text()
    error_dlg = ft.AlertDialog(title=error_t, bgcolor=ft.colors.ON_ERROR)

    DEFAULT_MESSAGE = "слива"

    def on_change(e):
        try:
            page.cipher = TrisemusSubstitutionCipher(
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

    def on_change_params(e):
        if message_tb.value != DEFAULT_MESSAGE:
            message_tb.value = ""
        shift_slider.value = 1
        page.update()
        on_change(e)

    use_punctiation_c = ft.Checkbox(
        label="Punctiation", value=True, on_change=on_change_params
    )
    use_numbers_c = ft.Checkbox(label="Numbers", value=True, on_change=on_change_params)
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
    message_tb.value = DEFAULT_MESSAGE
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
        keyword_tb,
        shift_slider,
        ft.Row(
            controls=[
                use_punctiation_c,
                use_numbers_c,
            ]
        ),
        ft.Divider(),
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
    message_tx.value = "пусть будет так, как мы хотели"
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
    decrypted_tx.value = page.cipher.decrypt(encrypted_tx.value)

    controls = [
        block_size_slider,
        ft.Divider(),
        message_tx,
        encrypted_tx,
        decrypted_tx,
    ]
    return controls


def block_cipher_controls(
    page: ft.Page,
) -> list[typing.Type["ft.Control"]]:
    def str_to_bytearray(data: str):
        return bytearray(data.encode())

    def bytearry_to_str(data: bytearray):
        return data.decode(errors="ignore")

    init_vect_str = "начальный вектор1"
    init_vect_bytearray = str_to_bytearray(init_vect_str)
    keyword_str = "секретный ключ 1234"
    keyword_bytearray = str_to_bytearray(keyword_str)
    page.encrypt_cipher_obj = GOST_34_13_2015_GammaOutputFeedback(
        key=keyword_bytearray, init_vect=init_vect_bytearray
    )
    page.decrypt_cipher_obj = GOST_34_13_2015_GammaOutputFeedback(
        key=keyword_bytearray, init_vect=init_vect_bytearray
    )
    error_t = ft.Text()
    error_dlg = ft.AlertDialog(title=error_t, bgcolor=ft.colors.ON_ERROR)

    DEFAULT_MESSAGE = "секретный текст"

    def fill_log_lv(e: ft.ControlEvent | None = None):
        for v in gost_34_13_2015.log_path.open("r").readlines():
            log_lv.controls.append(ft.Text(v))

    def on_change(e):
        try:
            init_vect_str = init_vect_tb.value
            init_vect_bytearray = str_to_bytearray(init_vect_str)
            keyword_str = keyword_tb.value
            keyword_bytearray = str_to_bytearray(keyword_str)
            page.encrypt_cipher_obj = GOST_34_13_2015_GammaOutputFeedback(
                key=keyword_bytearray, init_vect=init_vect_bytearray
            )
            page.decrypt_cipher_obj = GOST_34_13_2015_GammaOutputFeedback(
                key=keyword_bytearray, init_vect=init_vect_bytearray
            )
            encrypted_tb.value = page.encrypt_cipher_obj.encrypt(
                message_tb.value.encode()
            )
            decrypted_tb.value = page.decrypt_cipher_obj.decrypt(
                encrypted_tb.value
            ).decode()
            fill_log_lv(e)
        except Exception as e:
            logger.error(e)
            error_t.value = "\n".join(e.args)
            page.dialog = error_dlg
            error_dlg.open = True
        page.update()

    init_vect_tb = ft.TextField(
        label="Initial vector", value=init_vect_str, on_change=on_change
    )
    keyword_tb = ft.TextField(label="Key", value=keyword_str, on_change=on_change)
    message_tb = ft.TextField(
        label="Message",
        multiline=True,
        hint_text="Enter message to encrypt",
        on_change=on_change,
    )
    message_tb.value = DEFAULT_MESSAGE
    encrypted_tb = ft.TextField(
        label="Encrypted",
        read_only=True,
        multiline=True,
    )
    encrypted_tb.value = page.encrypt_cipher_obj.encrypt(message_tb.value.encode())
    decrypted_tb = ft.TextField(
        label="Decrypted",
        read_only=True,
        multiline=True,
    )
    decrypted_tb.value = page.decrypt_cipher_obj.decrypt(encrypted_tb.value).decode()

    log_lv = ft.ListView(expand=True, spacing=0)
    fill_log_lv()
    controls = [
        ft.Row(
            controls=[
                ft.TextField(
                    label="Block size (bytes)",
                    value=page.encrypt_cipher_obj.block_size,
                    read_only=True,
                    width=140,
                ),
                ft.TextField(
                    label="Key size (bytes)",
                    value=page.encrypt_cipher_obj.key_size,
                    read_only=True,
                    width=140,
                ),
            ],
        ),
        keyword_tb,
        init_vect_tb,
        ft.Divider(),
        message_tb,
        encrypted_tb,
        decrypted_tb,
        ft.Divider(),
        log_lv
    ]
    return controls


def main(page: ft.Page):
    page.title = "Криптографические алгоритмы шифрования"
    page.window_width = 700
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
    page.window_center()

    def route_change(route):
        page.views.clear()
        c1 = ft.Container(
            content=ft.Column(
                [
                    ft.Image(
                        "replace.png",
                        fit=ft.ImageFit.FILL,
                    ),
                    ft.Text("Метод Замены. Шифр Трисемуса", size=20),
                ],
            ),
            margin=10,
            padding=10,
            alignment=ft.alignment.center,
            width=180,
            height=180,
            border_radius=10,
            ink=True,
            on_click=lambda _: page.go("/substitution_cipher"),
            bgcolor=ft.colors.SURFACE_VARIANT,
        )
        c2 = ft.Container(
            content=ft.Column(
                [
                    ft.Image(
                        "transpose.png",
                        fit=ft.ImageFit.FILL,
                    ),
                    ft.Text("Метод перестановки. Простая перестановка", size=20),
                ],
            ),
            margin=10,
            padding=10,
            alignment=ft.alignment.center,
            width=180,
            height=180,
            border_radius=10,
            ink=True,
            on_click=lambda _: page.go("/transposition_cipher"),
            bgcolor=ft.colors.SURFACE_VARIANT,
        )
        c3 = ft.Container(
            content=ft.Column(
                [
                    ft.Image(
                        "grasshooper.png",
                        fit=ft.ImageFit.FILL,
                    ),
                    ft.Text(
                        "Метод блочного шифрования Кузнечик",
                        size=20,
                    ),
                    ft.Text(
                        "в режиме гаммирования с обратной связью по выходу",
                    ),
                ],
            ),
            margin=10,
            padding=10,
            alignment=ft.alignment.center,
            width=180,
            height=180,
            border_radius=10,
            ink=True,
            on_click=lambda _: page.go("/block"),
            bgcolor=ft.colors.SURFACE_VARIANT,
        )
        page.views.append(
            ft.View(
                "/",
                [
                    ft.Container(
                        ft.Text("Методы шифрования", size=40),
                        alignment=ft.alignment.center,
                    ),
                    ft.Row(
                        controls=[c1, c2, c3],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
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
        elif page.route == "/block":
            page.views.append(
                ft.View(
                    "/block",
                    controls=[
                        ft.AppBar(
                            title=c3.content.controls[1],
                            bgcolor=ft.colors.SURFACE_VARIANT,
                        ),
                        *block_cipher_controls(page),
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

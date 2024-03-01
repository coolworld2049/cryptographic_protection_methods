import typing

import flet as ft
from loguru import logger

from cipher.transposition.algorithm import TranspositionCipher


def transposition_cipher_controls(
    page: ft.Page,
) -> list[typing.Type["ft.Control"]]:
    page.cipher = TranspositionCipher()

    def on_change(e):
        page.cipher = TranspositionCipher(
            block_size=int(block_size_slider.value),
        )
        logger.info(f"Initialize {page.cipher}")
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

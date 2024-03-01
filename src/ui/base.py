import flet as ft


class BaseCipherPage:
    page: ft.Page = ft.Page
    page.window_width = 600
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
    page.window_center()
    page.message_tx = ft.TextField(
        label="Message",
        multiline=True,
        hint_text="Enter message to encrypt",
    )
    page.encrypt_tx = ft.TextField(
        label="Encrypted",
        read_only=True,
        multiline=True,
    )
    page.decrypt_tx = ft.TextField(
        label="Decrypted",
        read_only=True,
        multiline=True,
    )

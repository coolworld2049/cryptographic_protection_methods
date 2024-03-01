import logging
import sys

import flet as ft
from loguru import logger

from ui.controls.substitution_cipher import substitution_cipher_controls
from ui.controls.transposition_cipher import transposition_cipher_controls

logger.remove()
logger.add(sys.stdout, level=logging.INFO)


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
                        "assets/gravity_falls.png",
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
                        "assets/scytale.png",
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
                        "assets/gamma.png",
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

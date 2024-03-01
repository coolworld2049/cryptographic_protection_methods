import flet as ft

from ui.controls.trisemus_replacement_cipher import trisemus_replacement_cipher_controls


def main(page: ft.Page):
    page.title = "Ciphers"
    page.window_width = 600
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
    page.window_center()

    def route_change(route):
        page.views.clear()
        c1 = ft.Container(
            content=ft.Text("Trisemus Replacement Cipher", size=20),
            margin=10,
            padding=10,
            alignment=ft.alignment.center,
            width=150,
            height=150,
            border_radius=10,
            ink=True,
            on_click=lambda _: page.go("/trisemus_replacement_cipher"),
        )
        c2 = ft.Container(
            content=ft.Text("Permutation Cipher", size=20),
            margin=10,
            padding=10,
            alignment=ft.alignment.center,
            width=150,
            height=150,
            border_radius=10,
            ink=True,
            on_click=lambda _: page.go("/permutation_cipher"),
        )
        c3 = ft.Container(
            content=ft.Text("Gamma Cipher", size=20),
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
        if page.route == "/trisemus_replacement_cipher":
            page.views.append(
                ft.View(
                    "/trisemus_replacement_cipher",
                    controls=[
                        ft.AppBar(title=c1.content, bgcolor=ft.colors.SURFACE_VARIANT),
                        *trisemus_replacement_cipher_controls(page),
                    ],
                )
            )
        elif page.route == "/permutation_cipher":
            page.views.append(
                ft.View(
                    "/permutation_cipher",
                    controls=[
                        ft.AppBar(title=c2.content, bgcolor=ft.colors.SURFACE_VARIANT),
                    ],
                )
            )
        elif page.route == "/gamma_cipher":
            page.views.append(
                ft.View(
                    "/gamma_cipher",
                    controls=[
                        ft.AppBar(title=c3.content, bgcolor=ft.colors.SURFACE_VARIANT),
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

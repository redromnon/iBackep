import flet as ft
import webbrowser as wb

WEBSITE_URL = "https://github.com/redromnon/iBackep"


@ft.component
def About(version: str):
    open, set_open = ft.use_state(False)

    description = (
        f"{version}\n\n"
        "iBackep is a lightweight GUI backup manager for Apple iPhone and iPad for Linux\n"
        "(GPL-3.0 License)\n\n"
        "Made with ❤️ by redromnon"
    )

    about_modal = ft.AlertDialog(
        title=ft.Text("About", text_align=ft.TextAlign.CENTER),
        content=ft.Column(
            [
                ft.Text(
                    description,
                    text_align=ft.TextAlign.CENTER,
                    theme_style=ft.TextThemeStyle.BODY_SMALL,
                    size=14,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            height=120,
        ),
        actions_alignment=ft.MainAxisAlignment.CENTER,
        actions=[ft.TextButton("Website", on_click=lambda e: wb.open(WEBSITE_URL))],
    )
    ft.use_dialog(about_modal if open else None)

    return ft.IconButton(
        icon=ft.Icons.QUESTION_MARK_ROUNDED,
        icon_size=18,
        tooltip="About",
        on_click=lambda e: set_open(True),
        icon_color=ft.Colors.WHITE_70,
    )

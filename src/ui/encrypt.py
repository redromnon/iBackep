import flet as ft


@ft.component
def EncryptField(password: str, on_password_change, on_change_password_request):
    help_open, set_help_open = ft.use_state(False)

    encrypt_help = ft.AlertDialog(
        title=ft.Text("Encryption Help", text_align=ft.TextAlign.CENTER),
        content=ft.Column(
            [
                ft.Text(
                    "You are required to enter the correct password if the backup is encrypted.",
                    text_align=ft.TextAlign.CENTER,
                    theme_style=ft.TextThemeStyle.BODY_SMALL,
                    size=13,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            height=50,
            width=200,
        ),
        actions=[ft.TextButton("Ok", on_click=lambda e: set_help_open(False))],
        modal=True,
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )
    ft.use_dialog(encrypt_help if help_open else None)

    return ft.Row(
        [
            ft.TextField(
                password=True,
                can_reveal_password=True,
                value=password,
                filled=False,
                border=ft.UnderlineInputBorder(),
                hint_text="Encryption password",
                width=300,
                on_change=lambda e: on_password_change(e.data),
            ),
            ft.IconButton(
                icon=ft.Icons.INFO_ROUNDED,
                icon_size=28,
                tooltip="Show encryption help",
                icon_color=ft.Colors.WHITE_70,
                on_click=lambda e: set_help_open(True),
            ),
            ft.IconButton(
                icon=ft.Icons.LOCK_ROUNDED,
                icon_size=28,
                tooltip="Change encryption password",
                icon_color=ft.Colors.WHITE_70,
                on_click=lambda e: on_change_password_request(),
            ),
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
    )

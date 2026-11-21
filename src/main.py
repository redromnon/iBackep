import logging

import flet as ft

from ui.app import App

version = "v3.0.0"

logging.basicConfig(level=logging.INFO)


def main(page: ft.Page):
    page.title = "iBackep"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.render(App, version)


ft.run(main)

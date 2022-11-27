import flet as ft
from ui import App


def main(page: ft.Page):

    page.title = "iBackep"
    page.vertical_alignment = "center"
    page.theme_mode = "system"

    ibackep = App()
    
    page.add(ibackep)
    

ft.app(target=main)
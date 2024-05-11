import flet as ft
from ui.app import App
from ui.about import get_version

version = "v1.1.1"

def main(page: ft.Page):

    page.title = "iBackep"
    page.vertical_alignment = "center"
    page.theme_mode = "dark"

    #Pass version to about
    get_version(version)
    
    #App title and version
    app_name = ft.Row(
        [
            ft.Text("iBackep", size = 56, weight="bold", color=ft.colors.WHITE),
            ft.Text(version, size = 20, weight=ft.FontWeight.NORMAL, color=ft.colors.WHITE)
        ], 
        alignment=ft.MainAxisAlignment.CENTER, 
    )
    page.add(app_name)
    
    ibackep = App()
    
    page.add(ibackep)
    

ft.app(target=main)
import flet as ft
from ui.app import App
from ui.about import get_version

version = "v0.3.0"

def main(page: ft.Page):

    page.title = "iBackep"
    page.vertical_alignment = "center"
    page.theme_mode = "system"

    #Pass version to about
    get_version(version)
    
    #App title and version
    app_name = ft.Row([ft.Text("iBackep", size = 56, weight="bold")], alignment="center")
    page.add(app_name)
    
    ibackep = App()
    
    page.add(ibackep)
    

ft.app(target=main)
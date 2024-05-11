import flet as ft
import webbrowser as wb

version = None
def get_version(v):
    global version
    version = v

class About(ft.UserControl):

    def build(self):

        global version
    
        self.desc = ( version + "\n\niBackep is a lightweight GUI backup manager for Apple iPhone and iPad for Linux\n" + 
            "(GPL-3.0 License)\n\nMade with ❤️ by redromnon"
        )
        
        
        self.about_icon = ft.IconButton(icon=ft.icons.QUESTION_MARK_ROUNDED, icon_size=18, 
            tooltip="About", on_click=self.display_about, icon_color=ft.colors.WHITE70
        )

        self.about_modal = ft.AlertDialog(title=ft.Text("About", text_align="center"), 
                            content=ft.Column(
                                [
                                    ft.Text(self.desc, text_align="center", theme_style="bodySmall", size=14),
                                ], horizontal_alignment="center", height=120,  
                            ),
                            actions_alignment="center",
                            actions=[ft.TextButton("Website", on_click=lambda e: wb.open("https://github.com/redromnon/iBackep")),]
                        )

        return ft.Stack([self.about_modal, self.about_icon])


    def display_about(self,e):
        self.about_modal.open = True
        self.update()
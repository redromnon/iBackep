import flet as ft
import webbrowser as wb

class About(ft.UserControl):

    def build(self):
    
        self.desc = (
            "iBackep is a lightweight GUI backup manager for Apple iPhone and iPad for Linux\n" + "(GPL-3.0 License)\n\n"
            "Made with ❤️ by redromnon"
        )
        
        
        self.about_icon = ft.IconButton(icon=ft.icons.QUESTION_MARK_ROUNDED, icon_size=18, 
                                        tooltip="About", on_click=self.display_about)

        self.about_modal = ft.AlertDialog(title=ft.Text("About", text_align="center"), 
                            content=ft.Column(
                                [
                                    ft.Text(self.desc, text_align="center", style="bodySmall", size=14),
                                    ft.TextButton("Website", on_click=lambda e: wb.open("https://github.com/redromnon/iBackep"))
                                ], horizontal_alignment="center", height=100
                            )
                        )

        return ft.Stack([self.about_modal, self.about_icon])


    def display_about(self,e):
        self.about_modal.open = True
        self.update()
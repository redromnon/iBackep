import flet as ft

class Encrypt(ft.UserControl):
    
    def build(self):

        self.password_field = ft.TextField(
            password=True, can_reveal_password=True, 
            filled=False, border=ft.InputBorder.UNDERLINE,
            hint_text="Encryption password"
        )

        self.info_button = ft.IconButton(
            icon=ft.icons.INFO_ROUNDED, icon_size=28, on_click=self.toggle_help, tooltip="Show encryption help",
            icon_color=ft.colors.WHITE70
        )

        self.encrypt_help = ft.AlertDialog(
            title=ft.Text("Encryption Help", text_align="center"),
            content=ft.Column(
                [
                    ft.Text("You are required to enter the correct password if the backup is encrypted.",
                            text_align="center", theme_style="bodySmall", size=13),
                ],
                horizontal_alignment="center", height=50, width=200
            ),
            actions=[ft.TextButton("Ok", on_click=self.toggle_help)], modal=True,
            actions_alignment=ft.MainAxisAlignment.CENTER 
        )

        return ft.Row([self.password_field, self.info_button, self.encrypt_help], spacing=10, alignment="center")


    def get_pwd(self):
                
        return self.password_field.value


    def toggle_help(self, e):

        if self.encrypt_help.open:
            self.encrypt_help.open=False
        else:
            self.encrypt_help.open=True
        
        self.update()

import flet as ft

class Encrypt(ft.UserControl):
    
    def build(self):

        self.encrypt_checkbox = ft.Checkbox(
            fill_color={ft.MaterialState.HOVERED: ft.colors.LIGHT_BLUE}, on_change=self.enable_checkbox,
            tooltip="Enable encryption"
        )

        self.password_field = ft.TextField(
            password=True, can_reveal_password=True, disabled=True, width=270, height=40, 
            content_padding=ft.padding.only(bottom=15, left=10), hint_text="Encryption password"
        )

        self.info_button = ft.IconButton(
            icon=ft.icons.INFO_ROUNDED, icon_size=28, on_click=self.toggle_help
        )

        self.encrypt_help = ft.AlertDialog(
            title=ft.Text("Encryption Help", text_align="center"),
            content=ft.Column(
                [
                    ft.Text("Your backup can be protected by encrypting it with a password. Just enable the checkbox and type your password.\n\n" +
                            "When performing a BACKUP, you need to set a password and encrypt it for the first time only." +
                            " There's no need to insert the password every time once it's already encrypted.\n\n" +
                            "When performing a RESTORE however, you will need to insert the password every single time.",
                            text_align="center", style="bodySmall"),
                ],
                horizontal_alignment="center", height=120, width=500
            ),
            actions=[ft.TextButton("Ok", on_click=self.toggle_help)], modal=True 
        )

        return ft.Row([self.encrypt_checkbox, self.password_field, self.info_button, self.encrypt_help], spacing=10, alignment="center")

    
    def enable_checkbox(self,e):
        
        if self.encrypt_checkbox.value:
        
            self.password_field.disabled=False
            self.update()

        else:

            self.password_field.disabled=True
            self.update()

    def get_pwd(self):

        if self.encrypt_checkbox.value:

            if len(self.password_field.value) > 0:
                
                return self.password_field.value

    def toggle_help(self, e):

        if self.encrypt_help.open:
            self.encrypt_help.open=False
        else:
            self.encrypt_help.open=True
        
        self.update()

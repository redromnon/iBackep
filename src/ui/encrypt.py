import flet as ft

class Encrypt(ft.UserControl):
    
    def build(self):

        self.encrypt_checkbox = ft.Checkbox(
            fill_color={ft.MaterialState.HOVERED: ft.colors.LIGHT_BLUE}, on_change=self.enable_checkbox,
            tooltip="Enable encryption"
        )

        self.password_field = ft.TextField(
            password=True, can_reveal_password=True, disabled=True, width=275, height=40, 
            content_padding=ft.padding.only(bottom=15, left=10), hint_text="Encryption password"
        )

        return ft.Row([self.encrypt_checkbox, self.password_field], spacing=10, alignment="center")

    
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

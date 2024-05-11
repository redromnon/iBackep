import flet as ft, time, traceback

class Operation(ft.UserControl):
    
    def build(self):
                        
        self.close_button = ft.TextButton("Close", disabled=True, on_click=self.close_dialog)

        self.loading = ft.ProgressRing(value=None, width=60, height=60, stroke_width=5, bgcolor=ft.colors.GREY, color=ft.colors.WHITE)
        
        self.modal_dialog = ft.AlertDialog(
            content=ft.Container(
                content=self.loading, 
                alignment=ft.alignment.center, height=100, width=100
            ),
            content_padding=30, modal=True, 
            actions=[self.close_button], actions_alignment=ft.MainAxisAlignment.CENTER
        )

        return self.modal_dialog


    def _after_operations(self): #Enable UI after operation is successful
        self.close_button.disabled = False
        self.update()


    def backup(self, folder, pwd, service, is_first_backup):

        self.modal_dialog.open = True
        self.modal_dialog.title = ft.Text("Backup", text_align="center")
        self.update()

        #run process
        try:
            service.backup(
                backup_directory=folder,
                progress_callback=self.progressbar,
                full=is_first_backup
            )
        except:
            print(traceback.format_exc())
            self.close_dialog()
            return False
        else:
            self._after_operations()
            return True
    
    def restore(self, folder, pwd, service, identifier):

        self.modal_dialog.open = True
        self.modal_dialog.title = ft.Text("Restore", text_align="center")
        self.update()

        #run process
        try:
            service.restore(
                backup_directory=folder,
                progress_callback=self.progressbar,
                password=pwd,
                source=identifier
            )
        except:
            print(traceback.format_exc())
            self.close_dialog()
            return False
        else:
            self._after_operations()
            return True


    def close_dialog(self, e=None):

        #Reset properties to default
        self.close_button.disabled = True
        self.loading.value = None
        self.modal_dialog.open = False
        self.update()

    def progressbar(self, e):
        print(e)
        self.loading.value = round(e)/100
        self.loading.update()
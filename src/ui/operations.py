import flet as ft, time
import pymobiledevice3.services.mobilebackup2

class Operation(ft.UserControl):
    
    def build(self):
                        
        self.close_button = ft.TextButton("Close", disabled=True, on_click=self.close_dialog)

        self.loading = ft.ProgressBar(value=None)

        self.progress_tracker = ft.Text(value="Finished", weight=ft.FontWeight.W_300, size=15, visible=False)
        
        self.modal_dialog = ft.AlertDialog(
            content=ft.Column(
                [
                    self.progress_tracker, self.loading
                ], width=600, horizontal_alignment="center", alignment="center",
            ),
            content_padding=30, modal=True,
            actions=[self.close_button], actions_alignment=ft.MainAxisAlignment.CENTER
        )

        return self.modal_dialog

    def backup(self, folder, pwd, client):

        self.modal_dialog.open = True
        self.modal_dialog.title = ft.Text("Backup", text_align="center")
        self.update()

        #actual process
        backup_service = pymobiledevice3.services.mobilebackup2.Mobilebackup2Service(lockdown=client)
        backup_service.backup(
            backup_directory=folder,
            progress_callback=self.progressbar
        )

        backup_service = None
        self.progress_tracker.visible = True
        self.close_button.disabled = False
        self.update()

    
    def restore(self, folder, pwd, client):

        self.modal_dialog.open = True
        self.modal_dialog.title = ft.Text("Restore", text_align="center")
        self.update()

        #actual process
        restore_service = pymobiledevice3.services.mobilebackup2.Mobilebackup2Service(lockdown=client)
        restore_service.restore(
            backup_directory=folder,
            progress_callback=self.progressbar,
            password=pwd,
            source=client.identifier
        )

        restore_service = None
        self.progress_tracker.visible = True
        self.close_button.disabled = False
        self.update()


    def close_dialog(self, e):

        #Reset properties to default
        self.close_button.disabled = True
        self.loading.value = None
        self.modal_dialog.open = False
        self.progress_tracker.visible = False
        self.update()

    def progressbar(self, e):
        print(e)
        self.loading.value = round(e)/100
        self.loading.update()
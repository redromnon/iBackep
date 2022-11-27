import flet as ft
from libutilities import scan, Action

class App(ft.UserControl): 
    
    #Must func
    def build(self):
    
        #Action (operations - backup, restore and cancel) obj to used later
        self.action = Action()
        

        #App title
        self.app_name = ft.Text("iBackep", size=56, style="titleLarge")


        #Action (pop-up) dialogs
        self.backup_dialog = ft.AlertDialog(
            title=ft.Text("Backing Up Device", text_align="center"), 
            content=ft.Column(
                [ft.Text("This will take some time"), ft.ProgressRing()],
                height=50, horizontal_alignment="center"
            ),
            actions=[ft.TextButton("Cancel", on_click=self.cancel_op)],
            content_padding=40, modal=True
        )

        self.restore_dialog = ft.AlertDialog(
            title=ft.Text("Restoring Device", text_align="center"), 
            content=ft.Column(
                [ft.Text("This will take some time"), ft.ProgressRing()],
                height=50, horizontal_alignment="center"
            ),
            actions=[ft.TextButton("Cancel", on_click=self.cancel_op)],
            content_padding=40, modal=True
        )


        #Snackbar (bottom) dialog
        self.no_device_dialog = ft.SnackBar(content=ft.Text("No device found"))
        

        #Banner dialog
        self.backup_banner = ft.Banner(
            leading=ft.Icon(ft.icons.DONE_ROUNDED),
            actions=[ft.TextButton("Ok", on_click=self.close_banner)]
        )
        
        self.restore_banner = ft.Banner(
            leading=ft.Icon(ft.icons.DONE_ROUNDED),
            actions=[ft.TextButton("Ok", on_click=self.close_banner)]
        )


        #Folder
        self.folder_picker = ft.FilePicker(on_result=self.folder_dialog_result)
        
        self.display_folderpath = ft.TextField(
            hint_text="Select folder icon", width=400, read_only=False, border="none", 
            filled=True, max_lines=3
        )

        self.select_folder_icon = ft.IconButton(
            icon=ft.icons.FOLDER_ROUNDED, tooltip="Select folder location", 
            icon_size=36, on_click=lambda e: self.folder_picker.get_directory_path()
        )

        
        #Options
        self.backupbtn = ft.ElevatedButton(
            "Backup", icon=ft.icons.SETTINGS_BACKUP_RESTORE_ROUNDED, on_click=self.do_backup,
            disabled=True
        )

        self.restorebtn = ft.ElevatedButton(
            "Restore", icon=ft.icons.RESTORE_ROUNDED, on_click=self.do_restore,
            disabled=True
            )


        
        #UI component groups
        self.folder_container = ft.Row(
            [self.display_folderpath, self.select_folder_icon, self.folder_picker], 
            spacing=10, alignment="center"
        )
        
        self.options_container = ft.Row(
            [self.backupbtn, self.restorebtn], spacing=50, alignment="center")
        
        self.main_container = ft.Column(
            [self.backup_banner, self.backup_dialog, self.app_name, self.folder_container, 
            self.options_container, self.restore_dialog, self.no_device_dialog, self.restore_banner], 
            spacing=35, horizontal_alignment="center"
        )

        
        return self.main_container



    #Display folder path in textfield and enable options
    def folder_dialog_result(self, e: ft.FilePickerResultEvent):
        
        self.display_folderpath.value = e.path

        self.backupbtn.disabled = False
        self.restorebtn.disabled = False

        self.update()
    
    
    #Close action finished banner
    def close_banner(self, e):
        
        if(self.backup_banner.open):
            self.backup_banner.open = False
        elif(self.restore_banner.open):
            self.restore_banner.open = False

        self.update()
    
    
    #Call backup/restore/cancel actions    
    def do_backup(self, e):

        #check for device
        status = scan()

        if status:
            print("Device found!")

            #Display backup alert progress dialog
            self.backup_dialog.open = True
            self.update()

            #Run backup operation
            print("Backup running...")
            self.action.backup(self.display_folderpath.value)

            #Successfully executed with return code as 0
            if self.action.process.poll() == 0:
                self.backup_dialog.open = False 

                self.backup_banner.content = ft.Text("Backup successfully finished")
                self.backup_banner.open = True

                print("Backup successfully finished")

                self.update()
            else:
                self.backup_dialog.open = False 

                self.backup_banner.content = ft.Text("Something went wrong")
                self.backup_banner.open = True

                print("Something went wrong")

        else:
            self.no_device_dialog.open = True
            self.update()


    def do_restore(self, e):
        
        #check for device
        status = scan()

        if status:
            print("Device found!")

            #Display backup alert progress dialog
            self.restore_dialog.open = True
            self.update()

            #Run restore operation
            print("Restore running...")
            self.action.restore(self.display_folderpath.value)

            #Successfully executed with return code as 0
            if self.action.process.poll() == 0:
                self.restore_dialog.open = False

                self.restore_banner.content = ft.Text("Restore successfully finished")
                self.restore_banner.open = True

                print("Restore successfully finished")

                self.update()
            else:
                self.restore_dialog.open = False

                self.restore_banner.content = ft.Text("Something went wrong")
                self.restore_banner.open = True

                print("Something went wrong")

                self.update()
        else:
            self.no_device_dialog.open = True
            self.update()


    def cancel_op(self, e):

        self.action.cancel()

        #close alert dialogs
        if(self.backup_dialog.open):
            
            self.backup_dialog.open = False

            self.backup_banner.content = ft.Text("Backup cancelled")
            self.backup_banner.open = True

            print("Backup cancelled")

        elif(self.restore_dialog.open):
            
            self.restore_dialog.open = False

            self.restore_banner.content = ft.Text("Restore cancelled")
            self.restore_banner.open = True

            print("Restore cancelled")

        self.update()


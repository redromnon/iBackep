import flet as ft, traceback
from ui.about import About
from ui.encrypt import Encrypt
from ui.operations import Operation
import pymobiledevice3.lockdown, pymobiledevice3.exceptions, pymobiledevice3.services.mobilebackup2

class App(ft.UserControl): 
    
    #Must func
    def build(self):
    
        #Import about dialog
        self.about_button = About()

        #Import encryption password container row
        self.pwd_encrypt = Encrypt()

        #Process dialog for Action
        self.operation_dialog = Operation()


        #Snackbar (bottom) dialog
        self.no_device_dialog = ft.SnackBar(content=ft.Text("No device found"))

        self.no_folder_selected_dlg = ft.SnackBar(content=ft.Text("Please select a destination folder using the folder icon"))


        #Folder
        self.folder_picker = ft.FilePicker(on_result=self.folder_dialog_result)
        
        self.display_folderpath = ft.TextField(
            hint_text="Select folder icon", width=400, read_only=True, border="none", 
            filled=True, max_lines=3, color="#a6a6a6"
        )

        self.select_folder_icon = ft.IconButton(
            icon=ft.icons.FOLDER_ROUNDED, tooltip="Select folder location", 
            icon_size=36, on_click=lambda e: self.folder_picker.get_directory_path()
        )

        
        #Options
        self.backupbtn = ft.ElevatedButton(
            "Backup", icon=ft.icons.SETTINGS_BACKUP_RESTORE_ROUNDED, 
            on_click=lambda e: self.call_operations(backup=True),
            disabled=False
        )

        self.restorebtn = ft.ElevatedButton(
            "Restore", icon=ft.icons.RESTORE_ROUNDED, 
            on_click=lambda e: self.call_operations(restore=True),
            disabled=False
            )


        
        #UI component groups
        self.folder_container = ft.Row(
            [self.display_folderpath, self.select_folder_icon, self.folder_picker], 
            spacing=10, alignment="center"
        )
        
        self.options_container = ft.Row(
            [self.backupbtn, self.restorebtn], spacing=20, alignment="center")
        
        
        #Main Container
        self.main_container = ft.Stack(
            [
                #Alerts and dialogs go here
                self.operation_dialog, self.no_device_dialog, self.no_folder_selected_dlg,

                #Others
                ft.Column(
                    [self.folder_container, self.pwd_encrypt, self.options_container, self.about_button], 
                    spacing=30, horizontal_alignment="center"
                )
            ]
        )

        
        return self.main_container



    #Display folder path in textfield and enable options
    def folder_dialog_result(self, e: ft.FilePickerResultEvent):
        
        self.display_folderpath.value = e.path

        self.update()
    

    #Call backup/restore/cancel actions 
    def call_operations(self, backup=False, restore=False):

        #check if folder path is specified and run operation
        if(len(self.display_folderpath.value) == 0):
            
            self.no_folder_selected_dlg.open = True
            self.update()

            return
        
        try:#to connect to device via USB and perform operations
            lockdown_client = pymobiledevice3.lockdown.create_using_usbmux()
            print(lockdown_client.display_name)
            service = pymobiledevice3.services.mobilebackup2.Mobilebackup2Service(lockdown=lockdown_client)

            pwd = self.pwd_encrypt.get_pwd()#Check if password is given

            if backup:
                #Run backup operation
                print("Backup running...")
                self.operation_dialog.backup(self.display_folderpath.value, pwd, service)

                self.update()

            if restore:
                #Run restore operation
                print("Restore running...")
                self.operation_dialog.restore(self.display_folderpath.value, pwd, service, lockdown_client.identifier)

                self.update() 

            lockdown_client = None
            service = None 

        except pymobiledevice3.exceptions.ConnectionFailedToUsbmuxdError:
            print(traceback.format_exc())
            self.no_device_dialog.open = True
            self.update()

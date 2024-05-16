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

        self.error_message_dlg = ft.SnackBar(content=None)

        #Folder
        self.folder_picker = ft.FilePicker(on_result=self.folder_dialog_result)
        
        self.display_folderpath = ft.TextField(
            hint_text="Select folder icon", width=400, read_only=True, border="none", 
            filled=True, max_lines=3, color=ft.colors.WHITE70
        )

        self.select_folder_icon = ft.IconButton(
            icon=ft.icons.FOLDER_ROUNDED, tooltip="Select folder location", 
            icon_size=36, on_click=lambda e: self.folder_picker.get_directory_path(),
            icon_color=ft.colors.WHITE70
        )

        
        #Options
        self.backupbtn = ft.ElevatedButton(
            "Backup", icon=ft.icons.SETTINGS_BACKUP_RESTORE_ROUNDED, 
            on_click=lambda e: self.call_operations(backup=True),
            disabled=False, style=ft.ButtonStyle(shape=ft.StadiumBorder(), padding=15),
            icon_color=ft.colors.BLACK87, color=ft.colors.BLACK87, bgcolor=ft.colors.WHITE
        )

        self.restorebtn = ft.ElevatedButton(
            "Restore", 
            icon=ft.icons.RESTORE_ROUNDED, 
            on_click=lambda e: self.call_operations(restore=True),
            disabled=False, style=ft.ButtonStyle(shape=ft.StadiumBorder(), padding=15),
            icon_color=ft.colors.BLACK87, color=ft.colors.BLACK87, bgcolor=ft.colors.WHITE
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
                self.operation_dialog, self.no_device_dialog, self.no_folder_selected_dlg, self.error_message_dlg,

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
        
        #Disable buttons
        self.backupbtn.disabled = True
        self.restorebtn.disabled = True
        self.update()
        
        #to connect to device via USB and perform operations
        try:
            #Create lockdown client
            lockdown_client = pymobiledevice3.lockdown.create_using_usbmux()
            print(lockdown_client.display_name)
        #handle exception where device is not available
        except:
            print(traceback.format_exc())
            self.no_device_dialog.open = True
            self.update()
        #run operations if lockdown client creation is successful
        else:
            #Create backup/restore service
            service = pymobiledevice3.services.mobilebackup2.Mobilebackup2Service(lockdown=lockdown_client)

            #Check if password is given
            pwd = self.pwd_encrypt.get_pwd()

            backup_exists = self.operation_dialog.check_if_backup_exists(self.display_folderpath.value)
            print('New backup folder?:', backup_exists)

            if backup:
                #Run backup operation
                print("Backup running...")
                status = self.operation_dialog.backup(self.display_folderpath.value, pwd, service, backup_exists)

                if status is False:
                    self.error_message_dlg.content = ft.Text("Backup failed")
                    self.error_message_dlg.open = True

                self.update()

            if restore:
                #Run restore operation
                print("Restore running...")
                status = self.operation_dialog.restore(self.display_folderpath.value, pwd, service, lockdown_client.identifier)

                if status is False:
                    self.error_message_dlg.content = ft.Text("Restore failed: Enter correct password for the encrypted backup")
                    self.error_message_dlg.open = True

                self.update() 

            lockdown_client = None
            service = None 
            backup_service = None
            pwd = None
        finally:
            #Renable buttons
            self.backupbtn.disabled = False
            self.restorebtn.disabled = False
            self.update()
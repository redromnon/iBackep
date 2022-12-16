import flet as ft
from libutilities import scan
from ui.about import About
from ui.encrypt import Encrypt
from ui.operations import Operation

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
        

        #Banner dialog
        self.lib_not_installed_banner = ft.Banner(
            content=ft.Text("Looks like libimobiledevice or libimobiledevice-utils is not installed"),
            actions=[ft.TextButton("Ok", on_click=self.close_banner)]
        )


        #Folder
        self.folder_picker = ft.FilePicker(on_result=self.folder_dialog_result)
        
        self.display_folderpath = ft.TextField(
            hint_text="Select folder icon", width=400, read_only=True, border="none", 
            filled=True, max_lines=3
        )

        self.select_folder_icon = ft.IconButton(
            icon=ft.icons.FOLDER_ROUNDED, tooltip="Select folder location", 
            icon_size=36, on_click=lambda e: self.folder_picker.get_directory_path()
        )

        
        #Options
        self.backupbtn = ft.ElevatedButton(
            "Backup", icon=ft.icons.SETTINGS_BACKUP_RESTORE_ROUNDED, on_click=self.do_backup,
            disabled=False
        )

        self.restorebtn = ft.ElevatedButton(
            "Restore", icon=ft.icons.RESTORE_ROUNDED, on_click=self.do_restore,
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
                self.lib_not_installed_banner, self.operation_dialog,
                self.no_device_dialog, self.no_folder_selected_dlg,

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
    
    
    #Close action finished banner
    def close_banner(self, e):
        
        if(self.backup_cancel_banner.open):
            self.backup_cancel_banner.open = False
        elif(self.restore_cancel_banner.open):
            self.restore_cancel_banner.open = False
        elif(self.lib_not_installed_banner.open):
            self.lib_not_installed_banner.open = False

        self.update()
    
    
    #Call backup/restore/cancel actions    
    def do_backup(self, e):

        #check if folder path is specified
        if(len(self.display_folderpath.value) == 0):
            
            self.no_folder_selected_dlg.open = True
            self.update()

            return

        
        #check if lib is installed & device is connected
        lib_installed, status = scan()

        if lib_installed and status:
            print("Device found!")

            #Run backup operation
            print("Backup running...")
            pwd = self.pwd_encrypt.get_pwd()#Check if password is given
            self.operation_dialog.backup(self.display_folderpath.value, pwd)

        elif lib_installed and not status:
            self.no_device_dialog.open = True
            self.update()

        else:
            self.lib_not_installed_banner.open = True

            self.update()


    def do_restore(self, e):
        
        #check if folder path is specified
        if(len(self.display_folderpath.value) == 0):
            
            self.no_folder_selected_dlg.open = True
            self.update()

            return
        

        #check if lib is installed & device is connected
        lib_installed, status = scan()

        if lib_installed and status:
            print("Device found!")

            #Run restore operation
            print("Restore running...")
            pwd = self.pwd_encrypt.get_pwd()#Check if password is given
            self.operation_dialog.restore(self.display_folderpath.value, pwd)

        elif lib_installed and not status:
            self.no_device_dialog.open = True
            self.update()

        else:
            self.lib_not_installed_banner.open = True

            self.update()        


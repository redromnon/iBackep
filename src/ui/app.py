import logging

import flet as ft
from pymobiledevice3.exceptions import (
    ConnectionFailedToUsbmuxdError,
    DeviceNotFoundError,
    InvalidBackupPasswordError,
    NoDeviceConnectedError,
    PasswordRequiredError,
)

import device
from ui.about import About
from ui.encrypt import EncryptField
from ui.operations import OperationDialog

logger = logging.getLogger(__name__)

NO_DEVICE_ERRORS = (ConnectionFailedToUsbmuxdError, DeviceNotFoundError, NoDeviceConnectedError)


@ft.component
def App(version: str):
    page = ft.context.page

    folder_path, set_folder_path = ft.use_state("")
    password, set_password = ft.use_state("")
    busy, set_busy = ft.use_state(False)
    status, set_status = ft.use_state("")
    progress, set_progress = ft.use_state(None)
    finished, set_finished = ft.use_state(False)
    dialog_open, set_dialog_open = ft.use_state(False)
    pwd_dialog_open, set_pwd_dialog_open = ft.use_state(False)
    old_pwd, set_old_pwd = ft.use_state("")
    new_pwd, set_new_pwd = ft.use_state("")

    picker = ft.use_memo(ft.FilePicker, [])

    def on_progress(pct):
        set_progress(round(pct) / 100)

    def show_snack(message: str, bgcolor=None):
        page.show_dialog(
            ft.SnackBar(content=ft.Text(message, color=ft.Colors.WHITE), bgcolor=bgcolor)
        )

    def close_operation(e=None):
        set_dialog_open(False)
        set_finished(False)
        set_progress(None)

    async def select_folder(e):
        path = await picker.get_directory_path()
        if path:
            set_folder_path(path)

    async def run_with_dialog(status: str, fail_noun: str, op):
        set_busy(True)
        set_status(status)
        set_progress(None)
        set_finished(False)
        set_dialog_open(True)
        try:
            await op()
            set_status(status + " — Finished")
            set_finished(True)
        except NO_DEVICE_ERRORS:
            logger.exception("No device connected")
            close_operation()
            show_snack("No device found", ft.Colors.RED_500)
        except InvalidBackupPasswordError:
            logger.exception("Wrong backup password")
            close_operation()
            show_snack(
                f"{fail_noun} failed: Enter correct password for the encrypted backup",
                ft.Colors.RED_500,
            )
        except PasswordRequiredError:
            logger.exception("Device is passcode protected")
            close_operation()
            show_snack(
                "Device is passcode protected - unlock it and try again",
                ft.Colors.RED_500,
            )
        except Exception:
            logger.exception("%s failed", fail_noun)
            close_operation()
            show_snack(f"{fail_noun} failed", ft.Colors.RED_500)
        finally:
            set_busy(False)

    async def perform(mode: str):
        if len(folder_path) == 0:
            show_snack("Please select a destination folder using the folder icon")
            return

        if mode == "backup":
            await run_with_dialog(
                "Backing Up", "Backup", lambda: device.run_backup(folder_path, on_progress)
            )
        else:
            await run_with_dialog(
                "Restoring",
                "Restore",
                lambda: device.run_restore(folder_path, password, on_progress),
            )

    def open_password_dialog(e=None):
        set_old_pwd(password)
        set_new_pwd("")
        set_pwd_dialog_open(True)

    def close_password_dialog(e=None):
        set_pwd_dialog_open(False)

    async def apply_password_change(e=None):
        set_pwd_dialog_open(False)
        await run_with_dialog(
            "Changing Password",
            "Password change",
            lambda: device.run_change_password(old_pwd, new_pwd),
        )

    async def start_backup(e):
        await perform("backup")

    async def start_restore(e):
        await perform("restore")

    change_password_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Change Password", text_align=ft.TextAlign.CENTER),
        content=ft.Column(
            [
                ft.TextField(
                    password=True,
                    can_reveal_password=True,
                    label="Old password",
                    value=old_pwd,
                    width=300,
                    on_change=lambda e: set_old_pwd(e.data),
                ),
                ft.TextField(
                    password=True,
                    can_reveal_password=True,
                    label="New password",
                    value=new_pwd,
                    width=300,
                    on_change=lambda e: set_new_pwd(e.data),
                ),
                ft.Text(
                    "Fill both fields to change the password.\n"
                    "Leave Old empty to enable encryption, or New empty to disable it.",
                    size=12,
                    color=ft.Colors.WHITE_70,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            tight=True,
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        actions=[
            ft.TextButton("Cancel", on_click=close_password_dialog, disabled=busy),
            ft.TextButton(
                "Apply",
                on_click=apply_password_change,
                disabled=busy or (len(old_pwd) == 0 and len(new_pwd) == 0),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )
    ft.use_dialog(change_password_dialog if pwd_dialog_open else None)

    backup_button = ft.FilledButton(
        content="Backup",
        icon=ft.Icons.SETTINGS_BACKUP_RESTORE_ROUNDED,
        on_click=start_backup,
        disabled=busy,
        color=ft.Colors.BLACK_87,
        bgcolor=ft.Colors.WHITE,
        icon_color=ft.Colors.BLACK_87,
        style=ft.ButtonStyle(shape=ft.StadiumBorder(), padding=15),
    )

    restore_button = ft.FilledButton(
        content="Restore",
        icon=ft.Icons.RESTORE_ROUNDED,
        on_click=start_restore,
        disabled=busy,
        color=ft.Colors.BLACK_87,
        bgcolor=ft.Colors.WHITE,
        icon_color=ft.Colors.BLACK_87,
        style=ft.ButtonStyle(shape=ft.StadiumBorder(), padding=15),
    )

    folder_display = ft.TextField(
        hint_text="Select folder icon",
        width=400,
        read_only=True,
        border=ft.NoInputBorder(),
        filled=True,
        max_lines=3,
        color=ft.Colors.WHITE_70,
        value=folder_path,
    )

    folder_icon = ft.IconButton(
        icon=ft.Icons.FOLDER_ROUNDED,
        tooltip="Select folder location",
        icon_size=36,
        on_click=select_folder,
        icon_color=ft.Colors.WHITE_70,
    )

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Text("iBackep", size=56, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text(version, size=20, weight=ft.FontWeight.NORMAL, color=ft.Colors.WHITE),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [folder_display, folder_icon],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            EncryptField(
                password,
                on_password_change=set_password,
                on_change_password_request=open_password_dialog,
            ),
            ft.Row(
                [backup_button, restore_button],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            About(version),
            OperationDialog(
                visible=dialog_open,
                status=status,
                progress=progress,
                finished=finished,
                on_close=close_operation,
            ),
        ],
        spacing=30,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

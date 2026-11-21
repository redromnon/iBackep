import tempfile
from collections.abc import Callable

from pymobiledevice3.lockdown import create_using_usbmux
from pymobiledevice3.services.mobilebackup2 import Mobilebackup2Service

ProgressCallback = Callable[[float], None]


async def run_backup(backup_directory: str, on_progress: ProgressCallback) -> None:
    """
    Back up the connected device into `backup_directory`.

    Performs an incremental backup when a previous one exists, a full
    backup otherwise.
    """
    async with await create_using_usbmux() as lockdown:
        async with Mobilebackup2Service(lockdown) as service:
            await service.backup(
                full=False,
                backup_directory=backup_directory,
                progress_callback=on_progress,
            )


async def run_restore(backup_directory: str, password: str, on_progress: ProgressCallback) -> None:
    """
    Restore the backup in `backup_directory` to the connected device.
    """
    async with await create_using_usbmux() as lockdown:
        async with Mobilebackup2Service(lockdown) as service:
            await service.restore(
                backup_directory=backup_directory,
                password=password or "",
                progress_callback=on_progress,
            )


async def run_change_password(old: str, new: str) -> None:
    """
    Change, enable, or disable the device's backup encryption password.

    `old` and `new` empty selects enable (`new` set) or disable (`old` set).
    """
    async with await create_using_usbmux() as lockdown:
        async with Mobilebackup2Service(lockdown) as service:
            with tempfile.TemporaryDirectory() as temp_dir:
                await service.change_password(backup_directory=temp_dir, old=old, new=new)

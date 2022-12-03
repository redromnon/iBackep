# iBackep
iBackep is a simple GUI backup manager for the Apple iPhone and iPad built using [Flet](https://github.com/flet-dev/flet). It is currently available for Linux. 

Under the hood, the program makes use of [libimobiledevice](https://github.com/libimobiledevice/libimobiledevice) for performing operations.

![iBackepv0 3 0](https://user-images.githubusercontent.com/74495920/205428592-d1a1158f-0904-499e-8f7c-b722f678863e.png)

**Note - This project is still under development**

### Requirements
You will need the following packages to be installed for the program to work:
- **libimobiledevice**
- **libimobiledevice-utils**

Run `idevicebackup2 -v` to check if it's already installed on your system. 

If it isn't, you can use the following commands to install the packages on your system.

#### Debian and Ubuntu-based distributions
`sudo apt-get install libimobiledevice6 libimobiledevice-utils`

#### Fedora
`sudo dnf install libimobiledevice libimobiledevice-utils`

#### Arch Linux-based distributions
`pacman -S libimobiledevice`

### Features
- Perform backup and restore operations (Tested on iPhone 5s)
- Encrypt backups
- Light and Dark themes support

### Roadmap
- Better UI
- Display information about previous backups
- Support for customized backup and restore operations
- Windows and macOS support

### Download
Head over to [Releases](https://github.com/redromnon/iBackep/releases) and download the latest version's executable.

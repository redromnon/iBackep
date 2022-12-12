<img alt="GitHub" src="https://img.shields.io/github/license/redromnon/ibackep?style=flat-square"> <img alt="GitHub release (latest SemVer including pre-releases)" src="https://img.shields.io/github/v/release/redromnon/ibackep?include_prereleases&style=flat-square"> <img alt="GitHub all releases" src="https://img.shields.io/github/downloads/redromnon/ibackep/total?color=green&style=flat-square"> <a href="https://www.buymeacoffee.com/redromnon" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="20" width="80"></a>

# iBackep
iBackep is a simple and lightweight GUI backup manager for the Apple iPhone and iPad built using [Flet](https://github.com/flet-dev/flet). It is currently available for Linux. 

Under the hood, the program makes use of [libimobiledevice](https://github.com/libimobiledevice/libimobiledevice) for performing operations.

![Screenshot from 2022-12-11 20-29-12](https://user-images.githubusercontent.com/74495920/206911097-a1cb58af-e7f3-4a21-8a7a-fc2afe16ee78.png)


### Requirements
You will need the following packages to be installed for the program to work:
- **libimobiledevice**
- **libimobiledevice-utils**

Run `idevicebackup2 -v` to check if it's already installed on your system. 

If it isn't, you can use the following commands to install the packages on your system.

#### Debian and Ubuntu-based distributions
```
sudo apt-get install libimobiledevice6 libimobiledevice-utils
```

#### Fedora
```
sudo dnf install libimobiledevice libimobiledevice-utils
```

#### Arch Linux-based distributions
```
pacman -S libimobiledevice
```

### Features
- Perform backup and restore operations (Tested on iPhone 5s)
- Encrypt backups
- Light and Dark themes support (Depending on the system theme)

### Roadmap
- Better UI
- Display information about previous backups
- Support for customized backup and restore operations
- Windows and macOS support

### Download
Head over to [Releases](https://github.com/redromnon/iBackep/releases) and download the latest version's executable.

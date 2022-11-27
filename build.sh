#Build executable using pyinstaller
thisdir=$(pwd)
cd src && pyinstaller main.py --onefile --strip --name ibackep --paths=$thisdir/src
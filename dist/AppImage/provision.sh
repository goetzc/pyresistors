#!/usr/bin/env bash
set -euxo pipefail

# Run as vagrant user
if [ $UID -eq 0 ]; then
  exec su vagrant "$0" -- "$@"
fi

ARCH="$(uname -m)"

export PATH="~/.local/bin/:$PATH"

has_cmd() { command -v "$1" > /dev/null 2>&1; }

sudo apt-get update

############################################################
# Download AppImageTool and LinuxDeploy
############################################################
has_cmd appstreamcli || sudo apt-get install -y tree appstream
mkdir -p $HOME/.local/bin && cd $HOME/.local/bin

APP="appimagetool-${ARCH}.AppImage"; has_cmd ${APP} || wget https://github.com/AppImage/AppImageKit/releases/download/continuous/${APP}
APP="linuxdeploy-${ARCH}.AppImage"; has_cmd ${APP} || wget https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/${APP}
chmod +x *.AppImage

############################################################
# Chroot
############################################################
# cd ~/
# sudo apt-get install -y unionfs-fuse
# wget https://raw.githubusercontent.com/boolean-world/appimage-resources/master/tempenv.sh
# sudo ./tempenv.sh setup

############################################################
# Create AppDir
############################################################
sudo apt-get install --no-install-recommends -y python3-pyqt5

cd /vagrant

# Copy AppRun
rsync -avh dist/AppImage/AppRun AppDir/

# Create AppDir and resolve dependencies
linuxdeploy-$ARCH.AppImage \
  --appdir AppDir \
  --icon-file icons/pyresistors.png \
  --desktop-file pyresistors.desktop \
  -l /usr/lib/x86_64-linux-gnu/libQt5Widgets.so.5 \
  -l /usr/lib/x86_64-linux-gnu/qt5/plugins/platforms/libqxcb.so \
  --executable /usr/bin/python3  # --output appimage

# Copy PyQt5 libraries
mkdir -p AppDir/usr/lib/python3/dist-packages/
rsync -avh --exclude='bearer' --exclude='*[Dd]esigner*' \
  /usr/lib/x86_64-linux-gnu/qt5/plugins AppDir/usr/lib/qt5/
rsync -avh --exclude='bearer' --exclude='*[Dd]esigner*' \
  /usr/lib/python3/dist-packages/PyQt5 AppDir/usr/lib/python3/dist-packages/

# Copy the application
mkdir -p AppDir/usr/share/pyresistors
rsync -avh {pyresistors.py,ui,lib,icons} AppDir/usr/share/pyresistors/
find AppDir/usr/share/pyresistors -type d -name __pycache__ -exec rm -r {} +;

############################################################
# Create AppImage
############################################################
appimagetool-$ARCH.AppImage AppDir

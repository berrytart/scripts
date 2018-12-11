#!/bin/bash

wget https://www.novatel.com/assets/Documents/Downloads/ngpsusbpackage.tar.gz
tar xvfz ngpsubpackage.tar.gz
cd ngpsubpackage
echo dgist3414! | sudo -S dpkg -i ngpsusb.deb
sudo modprobe ngpsusb
sudo apt-get install ros-kinetic-novatel-gps-driver
cd ..

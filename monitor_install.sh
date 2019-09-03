#!/bin/bash

cd ~
sudo apt-get update
sudo apt-get install libpng12-dev -y
sudo apt-get install python-pkg-resources python3-pkg-resources -y
sudo apt-get install -y i2c-tools -y
sudo apt-get install build-essential python-dev python-smbus python-pip -y
sudo apt-get install python-serial -y
sudo pip install adafruit-ads1x15
cd ~
sudo chmod 777 /home/pi/BMO_GBZ/Pngview/pngview1

if ! grep '^\/home\/pi\/BMO_GBZ\/battery_monitor.py \&' /etc/rc.local; then
    sudo sed -i '/\"exit 0\"/!s/exit 0/python \/home\/pi\/BMO_GBZ\/battery_monitor.py \&\nexit 0/g' /etc/rc.local
    echo 'battery monitor script added to startup.'
else
    echo 'battery monitor script already enabled at startup.'
fi

config_txt=/boot/config.txt
echo "Enabling i2c..."
if ! grep '^dtparam=i2c_arm=on' $config_txt; then
  echo 'dtparam=i2c_arm=on' >> $config_txt
else
  echo "i2c already enabled."
fi

etc_modules=/etc/modules
echo "Adding entries to $etc_modules..."
if ! grep '^i2c-bcm2708' $etc_modules; then
  echo 'i2c-bcm2708' >> $etc_modules
  echo 'i2c-dev' >> $etc_modules
else
  echo "etc_modules already set up."
fi

#!/bin/bash

cd ~
sudo apt-get update
sudo apt-get install python-gpiozero -y
sudo apt-get install libpng12-dev -y

sudo chmod 777 /home/pi/BMO_GBZ/Pngview/pngview
sudo chmod 777 /home/pi/BMO_GBZ/Pngview/pngview2
sudo chmod 777 /home/pi/BMO_GBZ/Pngview/pngview3

echo "80" > /home/pi/volume.state
echo 'True' >> /home/pi/BMO_GBZ/monitor_icon.state

if ! grep '^\/home\/pi\/BMO_GBZ\/monitor_button.py \&' /etc/rc.local; then
    sudo sed -i '/\"exit 0\"/!s/exit 0/python \/home\/pi\/BMO_GBZ\/monitor_button.py \&\nexit 0/g' /etc/rc.local
    echo 'added script to startup.'
fi

if ! grep '^\/home\/pi\/BMO_GBZ\/volume_buttons.py \&' /etc/rc.local; then
    sudo sed -i '/\"exit 0\"/!s/exit 0/python \/home\/pi\/BMO_GBZ\/volume_buttons.py \&\nexit 0/g' /etc/rc.local
    echo "digital volume script added to startup."
else
  echo "digital volume script already enabled in startup."
fi

if ! grep '^\/home\/pi\/BMO_GBZ\/shutdown.py \&' /etc/rc.local; then
    sudo sed -i '/\"exit 0\"/!s/exit 0/python \/home\/pi\/BMO_GBZ\/shutdown.py \&\nexit 0/g' /etc/rc.local
    echo 'added script to startup.'
fi

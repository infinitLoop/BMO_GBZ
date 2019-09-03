
sudo apt-get update -y
#sudo apt-get upgrade -y
sudo apt-get install libsdl2-mixer-dev -y

cd /home/pi
sudo git clone http://github.com/infinitLoop/Guardians_of_Sunshine

cd /home/pi/Guardians_of_Sunshine

sudo make

sudo mkdir /home/pi/RetroPie/roms/adventuretime

echo "cd /home/pi/Guardians_of_Sunshine\nsudo ./GuardiansOfSunshine\n" > /home/pi/RetroPie/roms/adventuretime/GuardiansOfSunshine.sh

sudo cp /etc/emulationstation/es_systems.cfg /opt/retropie/configs/all/emulationstation/es_systems.cfg

if ! grep '^<systemList>\n  <system>\n    <name>adventuretime' /home/pi/.emulationstation/es_systems.cfg; then
    sudo sed -i 's/<systemList>/<systemList>\n  <system>\n    <name>adventuretime<\/name>\n    <fullname>Adventure Time Games<\/fullname>\n    <path>\/home\/pi\/RetroPie\/roms\/adventuretime<\/path>\n    <extension>\.sh \.SH<\/extension>\n    <command>%ROM%<\/command>\n    <theme>adventuretime<\/theme>\n  <\/system>/g' /home/pi/.emulationstation/es_systems.cfg
fi

sudo chmod -R 777 /home/pi/Guardians_of_Sunshine

sudo cp /home/pi/Guardians_of_Sunshine/gamelist.xml /home/pi/RetroPie/roms/adventuretime/gamelist.xml
sudo cp /home/pi/Guardians_of_Sunshine/*.jpg /home/pi/RetroPie/roms/adventuretime

sudo chmod -R 777 /home/pi/RetroPie/roms/adventuretime

cd ~

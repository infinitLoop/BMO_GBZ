from os import system
from gpiozero import Button
from signal import pause
from time import sleep
from subprocess import check_call

# Location of perisitant state file
folder = "/home/pi/BMO_GBZ"
pngviewPath = "%s/Pngview" % folder
imagesFolder = "%s/images" % folder
configFile = "%s/gpio.config" % folder

#########

# Functions
def doShutdown():
    system("omxplayer -o alsa --po 00:00:01 --no-keys --no-osd " + folder + "/BMO_shutdown.mp3 &")
    print("shutting down...")
    showimage("BMO_OFF.png")
    sleep(3)
    shutdown()

def shutdown():
    check_call(['sudo', 'poweroff'])

def showimage(image):
    system(pngviewPath + "/pngview3 -b 0 -l 999999 " + imagesFolder + "/" + image + " &")

def killimages():
    system("sudo killall -q -15 pngview3")

#########

# Initial File Setup
doShutdownControl = False
try:
    with open(configFile,"r") as configuration: 
        for line in configuration:
            if "=" in line:
                (key, val) = line.split("=")
                key = key.strip()
                val = val.strip()
                if key == "DoShutdownControl":
                    doShutdownControl = (val == "True")
                elif key == "GPIO_Shutdown":
                    shutdownPin = int(str(val))

except:
    print("error loading configuration. check ~/BMO_GBZ/gpio.config settings.")
    exit(0)

# Button interupts
if doShutdownControl:
    shutdownButton = Button(shutdownPin)
    shutdownButton.when_pressed = doShutdown

pause()


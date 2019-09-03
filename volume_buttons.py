from os import system
from gpiozero import Button
from signal import pause
from time import sleep

# Initial volume setting
vState = 80
# PCM or Speaker (USB audio)
sType = "PCM"  
# Minimum/maximum volume and how much each press adjusts
vMin = 0
vMax = 100
vStep = 10
vSpeed = 0.32  # in seconds (lower is faster)

# Location of perisitant state file
folder = "/home/pi/BMO_GBZ"
pngviewPath = "%s/Pngview" % folder
imagesFolder = "%s/images" % folder
configFile = "%s/gpio.config" % folder
volumeState = "%s/volume.state" % folder

currentImage = -1
#########


# Functions
def volumeDown():
    global vState
    global currentImage
    if vState > vMin:
        vState = max(vMin, vState - vStep)
        system("amixer sset -q '" + sType  + "' " + str(vState) + "%")
        #pngview only allows 8 images, so just do these image changes
        if vState in [0,20,40,60,80,100]:
            if vState != currentImage:
                showimage("Volume" + str(vState) + ".png")
                currentImage = vState
        elif vState+10 != currentImage:
            showimage("Volume" + str(vState+10) + ".png")
            currentImage = vState+10
    elif currentImage != vState:
        showimage("Volume" + str(vState) + ".png")
        currentImage = vState

def volumeUp():
    global vState
    global currentImage
    if vState < vMax:
        vState = min(vMax, vState + vStep)
        system("amixer sset -q '" + sType +  "' " + str(vState) + "%")
        #pngview only allows 8 images, so just do these image changes
        if vState in [0,20,40,60,80,100]:
            if vState != currentImage:
                showimage("Volume" + str(vState) + ".png")
                currentImage = vState
        elif vState+10 != currentImage:
            showimage("Volume" + str(vState+10) + ".png")
            currentImage = vState+10
    elif currentImage != vState:
        showimage("Volume" + str(vState) + ".png")
        currentImage = vState

def showimage(image):
    system(pngviewPath + "/pngview2 -b 0 -l 999999 " + imagesFolder + "/" + image + " &")

def killimages():
    global currentImage
    currentImage = -1
    system("sudo killall -q -15 pngview2")

def readData(filepath):
    with open(filepath, 'rb') as file:
        return file.read()

def writeData(filepath):
    with open(filepath, 'wb') as file:
        file.write(str(vState))

def doVolume():
    while True:
        if volumeUpBtn.is_pressed:
            volumeUp()
            writeData(volumeState)
            sleep(vSpeed)
        elif volumeDownBtn.is_pressed:
            volumeDown()
            writeData(volumeState)
            sleep(vSpeed)
        else:
            killimages()
    else:
        killimages()

#########

# Initial File Setup
doVolumeControl = False
try:
    with open(configFile,"r") as configuration: 
        for line in configuration:
            if "=" in line:
                (key, val) = line.split("=")
                key = key.strip()
                val = val.strip()
                if key == "DoVolumeControl":
                    doVolumeControl = (val == "True")
                elif key == "GPIO_VolumeUp":
                    volumeUpPin = int(str(val))
                elif key == "GPIO_VolumeDown":
                    volumeDownPin = int(str(val))
except:
    print("error loading configuration. check ~/BMO_GBZ/gpio.config settings.")
    exit(0)

try:
    vState = int(readData(volumeState))
    system("amixer sset -q '" + sType + "' " + str(vState) + "%")
except:
    writeData(volumeState)
    system("amixer sset -q '" + sType + "' " + str(vState) + "%")

# Button interupts
if doVolumeControl:
    volumeUpBtn = Button(volumeUpPin)
    volumeDownBtn = Button(volumeDownPin)
    volumeUpBtn.when_pressed = doVolume
    volumeDownBtn.when_pressed = doVolume

pause()


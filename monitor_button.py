from os import system
from gpiozero import Button
from signal import pause
from time import sleep

# giving it a little delay when changing state
REFRESH_RATE = 2
currentImage = -1

# Location of perisitant state file
folder = "/home/pi/BMO_GBZ"
pngviewPath = "%s/Pngview" % folder
imagesFolder = "%s/images" % folder
configFile = "%s/gpio.config" % folder
monitorState = "%s/monitor_icon.state" % folder
batteryMonitor = "%s/battery_monitor.py" % folder

#########

# Functions
def toggleIcon():
    # toggle state
    global showIcon
    if(showIcon):
        print("hiding battery icon")
    else:
        print("showing battery icon")

    showIcon = (not showIcon)
    writeData(monitorState)
    # kill the current monitor
    system("sudo pkill -f \"python " + batteryMonitor + "\"")
    # reload monitor
    sleep((REFRESH_RATE/2))
    system("python " + batteryMonitor + " &")
    sleep((REFRESH_RATE/2))

def readData(filepath):
    with open(filepath, 'rb') as file:
        return file.read()

def writeData(filepath):
    with open(filepath, 'wb') as file:
        file.write(str(showIcon))

#########

# Initial File Setup
doMonitorControl = False
try:
    with open(configFile,"r") as configuration: 
        for line in configuration:
            if "=" in line:
                (key, val) = line.split("=")
                key = key.strip()
                val = val.strip()
                if key == "DoMonitorControl":
                    doMonitorControl = (val == "True")
                elif key == "GPIO_Monitor":
                    monitorPin = int(str(val))

except:
    print("error loading configuration. check ~/BMO_GBZ/gpio.config settings.")
    exit(0)

try:
    showIcon = readData(monitorState)
except:
    showIcon = True

# Button interupts
if doMonitorControl:
    monitorButton = Button(monitorPin, hold_time = 2)
    monitorButton.when_held = toggleIcon

pause()


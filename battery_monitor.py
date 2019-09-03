#!/usr/bin/python
from time import sleep
from os import system
from subprocess import check_output
import signal
import serial
import Adafruit_ADS1x15

# Set to True to write out voltage readings to screen
debug = False
debugLevel = 2  # set to 2 for more output

# Analog Sensor Type :: "ADC" (ADS-1X15) or "SERIAL" (Micro Controller)
monitorType = "ADC"

# ADS Type :: "1015" (12bit) or "1115" (16bit)
adsType = "1015"

# Serial port on controller (only when using SERIAL type)
serialPort = 1  # use getSerialPort() if you aren't sure
serialWrite = 1  # vs 9 
controlVoltage = 0  # use 1 for full voltage (5.1v) check

# Set to True to display low and critical battery animation overlay 
displayWarning = False
# Set to True to automatically shutdown on critical battery
autoShutdownLow = False

# Screen location
xLocation = 650
yLocation = 10

# Folder and file locations
folder = "/home/pi/BMO_GBZ"
stateFile = "%s/monitor_icon.state" % folder
pngView = "%s/Pngview/pngview1" % folder
iconFolder = "%s/images" % folder
videoPlayer = "/usr/bin/omxplayer"

REFRESH_RATE = 8.5 # how often to read voltage, in seconds
SAMPLE_RATE = 16 # times to sample voltage, for average reading
VOLT100 = 3.95 # full voltage
VOLT75 = 3.68
VOLT50 = 3.42 # halfway
VOLT25 = 3.12
VOLT0 = 2.9 # empty voltage
GAIN = 1  # analog input gain  (leave at 1 unless you have a reason)

## remove sampling delay from refresh rate
REFRESH_RATE -= (SAMPLE_RATE * 0.5)
## if we went negative, put us back positive
if REFRESH_RATE <= 0:
    REFRESH_RATE = 0.1
    if debug:
        print("REFRESH_RATE was not sufficient to cover SAMPLE_RATE (0.5s per sample) - Setting REFRESH_RATE to 0.1")

#########

# Functions
def changeicon(percent):
    system(pngView + " -b 0 -l 999999" + str(percent) + " -x " + str(xLocation) + " -y " + str(yLocation) + " " + iconFolder + "/" + "battery" + str(percent) + ".png &")
    if debug and debugLevel==2:
        print(pngView + " -b 0 -l 999999" + str(percent) + " -x " + str(xLocation) + " -y " + str(yLocation) + " " + iconFolder + "/" + "battery" + str(percent) + ".png &")
    out = check_output("ps aux | grep pngview1 | awk '{ print $2 }'", shell=True)
    nums = out.split('\n')
    for num in nums:
        system("sudo kill " + num)
        break

def endProcess(signalnum=None, handler=None):
    system("sudo killall pngview1")
    exit(0)

def readVoltage():
    if monitorType == "SERIAL":
        value = readSerial()
    else:
        value = ads.read_adc(0, gain=GAIN)
    return value

def readSerial():
    ser.write(str(serialWrite))
    time.sleep(0.3)
    x = float(ser.readline())
    return x

def convertVoltage(sensorValue):
    voltage = round(((float(sensorValue) * (VOLT100 + controlVoltage)) / adsDivisor), 4)
    return voltage

def checkVoltageStatus():
    global batteryStatus
    global displayWarning
    
    voltage = 0
    for x in range(1, SAMPLE_RATE):
        voltage += readVoltage()
        if debug and debugLevel==2:
            print("Sample: " + str(voltage))
        sleep(0.5)
        
    voltage = convertVoltage((voltage / SAMPLE_RATE))
    
    if debug:
        print("Voltage: " + str(voltage))
    
    if voltage <= VOLT0:
        if displayWarning:
            system(videoPlayer + " --no-osd --layer 999999  " + iconFolder + "/../lowbattshutdown.mp4 --alpha 160;")
            displayWarning = False
        if autoShutdownLow:
            system("sudo shutdown -h now")
        status = 0
    elif voltage > VOLT0 and voltage <= VOLT25:
        if displayWarning:
            system(videoPlayer + " --no-osd --layer 999999  " + iconFolder + "/../lowbattalert.mp4 --alpha 160")
            displayWarning = False
        status = 25
    elif voltage > VOLT25 and voltage <= VOLT50:
        status = 50
    elif voltage > VOLT50 and voltage <= VOLT75:
        status = 75
    else:
        status = 100
    
    if debug and debugLevel==2:
        print("status: " + str(status)) 
        print("showIcon: " + str(showIcon))       
    
    if batteryStatus != status and showIcon:
        changeicon(status)
    
    batteryStatus = status

def getSerialPort():
    for x in range(0, 3):
        try:
            port = serial.Serial('/dev/ttyACM' + str(x), 115200)
            if debug and debugLevel==2:
                print('Serial Port Located: ' + str(x))
            return port
        except serial.SerialException:
            continue
    else:
        print('Serial Port Not Located')

#########

# initial setup
showIcon = True
batteryStatus = 0

if monitorType == "SERIAL":
    adsDivisor = 1023.0
    controlVoltage = 1
    try:
        ser = serial.Serial('/dev/ttyACM' + str(serialPort), 115200)
    except serial.SerialException:
        print('Serial Port ACM' + str(serialPort) + ' Not Found')
elif adsType == "1115":
    ads = Adafruit_ADS1x15.ADS1115()
    adsDivisor = 32767.0
else:
    ads = Adafruit_ADS1x15.ADS1015()
    adsDivisor = 2047.0

signal.signal(signal.SIGTERM, endProcess)
signal.signal(signal.SIGINT, endProcess)
system(pngView + " -b 0 -l 299999 -x " + str(xLocation) + " -y " + str(yLocation) + " " + iconFolder + "/blank.png &")

# read and/or create showIcon toggle file
try:
    with open(stateFile, 'r') as f:
        showIcon = (f.read() == "True")
except IOError:
    with open(stateFile, 'w') as f:
        f.write("True")
    
# start monitoring
while True:
    try:
        checkVoltageStatus()
        sleep(REFRESH_RATE)
    except IOError:
        print('BATTERY MONITOR ERROR:: I2C could not be located. Check connections and model config.')
        exit(0)
    except serial.SerialException:
        print('Serial Port ACM' + str(serialPort) + ' Not Found')
        exit(0)


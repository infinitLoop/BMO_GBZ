# BMO_GBZ
BMO (Beemo!) from Adventure Time themed utilities for Gameboy Zero RetroPie builds.

![BMO_GBZ](/BMO_GBZ.jpg)

Custom stand design located here: https://www.thingiverse.com/thing:3855445

I have had the best luck with these builds, in general, using RetroPie 4.3:
https://github.com/RetroPie/RetroPie-Setup/releases/tag/4.3

However, I believe this should work with whatever the latest release is as well.


### Library Installation
Download the library and update permissions to allow scripts to execute:
```
cd ~ && sudo git clone http://github.com/infinitLoop/BMO_GBZ && sudo chmod 777 -R ~/BMO_GBZ

```


### Install BMO EmulationStation Theme
also located here: https://github.com/infinitLoop/BMO_ES_Theme

Install the BMO theme for ES (you will need to select it in the menu). Enable <b>Instant</b> transition for best effect.
```

sudo ~/BMO_GBZ/./theme_install.sh

```


### Install Splashscreen
Copy the "Who wants to play video games" splash screen to the proper folder (you will need to select it in the menu).
```

sudo cp ~/BMO_GBZ/WhoWantsToPlay640.mp4 ~/RetroPie/splashscreens/'Who Wants To Play Video Games.mp4'

```

### Install Guardians of Sunshine Game
also located here: https://github.com/infinitLoop/Guardians_of_Sunshine

Install the Adventure Time game and details for Emulationstation
```

sudo ~/BMO_GBZ/./gos_install.sh

```


### Install Battery Monitor icon
Install the battery monitor icon (requires an ADC hooked into the battery connection, such as an ADS-1015/ADS-1115 or arduino/pro-micro):
```

sudo ~/BMO_GBZ/./monitor_install.sh

```
if you need to adjust voltage settings or ADC type
```

sudo nano ~/BMO_GBZ/battery_monitor.py

```

### Install GPIO Controls 
Install options for digital volume, safe shutdown and a hotkey to change the visibility of the Battery Monitor icon with GPIO buttons:
```

sudo ~/BMO_GBZ/./gpio_controls_install.sh

```
Edit this file to enable/disable the controls and configure the GPIO pins
```

sudo nano ~/BMO_GBZ/gpio.config

```
by default it will be:
```
DoVolumeControl = True
DoMonitorControl = True
DoShutdownControl = True

GPIO_VolumeUp = 15
GPIO_VolumeDown = 14
GPIO_Monitor = 4
GPIO_Shutdown = 17
```


### Install Safe Shutdown

If you have a PSU or Safe Shutdown circuit that requires a signal during the software shutdown, run this to set up keep-alive/powerdown signal.  Update the pin from 27 if you are using a different one.
```

sudo echo 'dtoverlay=gpio-poweroff,gpiopin="27",active_low="y"' >> /boot/config.txt

``` 

### Fix Video Splash Screen for Digital Audio
Digital audio devices can cause a stutter and lack of audio on the intro splash screen.  Run one of these to fix it:
```
## RetroPie 4.3-

sudo sed -i 's/omxplayer -o both -b --layer 10000/omxplayer -o alsa -b --layer 10000/g' /opt/retropie/supplementary/splashscreen/asplashscreen.sh

## RetroPie 4.4+

sudo sed -i 's/omxplayer -o both -b --layer 10000/omxplayer -o alsa -b --layer 10000/g' /etc/init.d/asplashscreen
 ```

Be MOre @!

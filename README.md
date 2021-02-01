# PiRadio
A Raspberry Pi internet radio service using VLC and the web service Flask

This was designed to work as a service on a Raspberry Pi.

The radio takes in responses from the GPIO as inputs and displays to an external LCD screen. The service also runs a web page that controls the radio at the Pi's IP adress

## Dependencies
[VLC For Python](https://wiki.videolan.org/Python_bindings/)
```
sudo pip3 install python-vlc
```
[Flask](https://flask.palletsprojects.com/en/1.1.x/)
```
sudo pip3 install flask
```
I2C Tools (For Finding the Address of the LCD)
```
sudo apt-get install i2c-tools
```
## Setup
Download and install the dependencies

Download the files to a location you would like to have the project

Edit the Path in radio.py and piRadio.service to the absolute path of the project.

Edit the sname in radio.py if you want a custom station list

Edit the I2CBUS and ADDRESS in lcdLib.py to match your pi/lcd
Check you lcd Address with `i2cdetect -y 1`

Make radio.py and web.py executable:
```
sudo chmod +x radio.py web.py
```

Move the lcdLib.py file to the location you keep your Python packages

Run `python3 -m site --user-site` to get the path


Move the service file to `/etc/systemd/system`
```
mv piRadio.service /etc/systemd/system
``` 

Set up the service using `systemctl`
```
sudo systemctl daemon-reload 
sudo systemctl enable piRadio.service
```
This will reload the services and enable the piRadio to run on startup



## Usage/Behavior
The piRadio service will run after the Pi is conected to the internet

After the internet connection is verified it will begin playing the first station stored.

The current model uses 3 buttons: Next, Prev, and Pause.

When a station begins playing the name of the station will be displayed on the LCD display for 5 seconds then the LCD will blank and the backlight will be turned off to prevent screen burn.

## Finding Stations
To create custom stations a live audio stream must be found.

Either add the name and station to the stations.csv or make your own and change the radio.py file.

After changing the stations file the new station will not be avalible until after the Pi or the service is restarted.
## Credit
Initial Script Work-[Elijah1111](https://github.com/Elijah1111)

Volume and Web Assistance-[Jacob Hall](https://github.com/jacobwhall)

LCD Library-[DenisFromHR](https://gist.github.com/DenisFromHR/cc863375a6e19dce359d)

Some of the radio stations are independent broadcasters and survive off of donations. If you enjoy the sations content please consider donating at the respective stations webpage.

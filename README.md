# PiRadio
A Raspberry Pi internet radio service using VLC

This was designed to work as a service in the Raspberry Pi.

The radio takes in responses from the GPIO as inputs and displays to an external LCD screen
## Dependencies
[VLC For Python](https://wiki.videolan.org/Python_bindings/)
```
pip3 install python-vlc
```
## Setup
Download and install the dependencies

Download the files to a location you would like to have the project

Edit the Path in radio.py and piRadio.service to the absolute path of the project.
Edit the sname in radio.py if you want a custom station list

Make the radio.py executable by all:
```
sudo chmod +x radio.py 
```


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

Move the lcdLib.py file to the location you keep your Python packages

Run `python3 -m site --user-site` to get the path

Then reboot it should be ready to go


## Usage/Behavior
The piRadio service will run after the Pi is conected to the internet

After the internet connection is verified it will begin playing the first station stored.

The current model uses 3 buttons: Next, Prev, and Pause.

When a station begins playing the name of the station will be displayed on the LCD display for 5 seconds then the backlight will turn off and blank.

## Finding Stations
To create custom stations a live audio stream must be found.

Either add the name and station to the stations.csv or make your own and change the radio.py file.

After changing the stations file the new station will not be avalible until after the Pi is restarted.
## Credit
Initial Script Work-[Elijah1111](https://github.com/Elijah1111)

LCD Library-[DenisFromHR](https://gist.github.com/DenisFromHR/cc863375a6e19dce359d)

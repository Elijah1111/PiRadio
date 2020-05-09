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



## Usage

## Credit
Initial Script Work-[Elijah1111](https://github.com/Elijah1111)

LCD Library-[DenisFromHR](https://gist.github.com/DenisFromHR/cc863375a6e19dce359d)

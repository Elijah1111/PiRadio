#!/usr/bin/env python3


import lcdLib as LCD
import vlc
import RPi.GPIO as gp
import time
import os


Path = "/home/pi/Documents/radio/"#TODO
sname = "stations.csv"#TODO


def playing(s="Paused"):#Write the currently playing station
    with open(Path+"playing.txt",'w') as f:
        print(s, file=f)
        f.close()


def write(lcd=LCD.lcd(),s=''):#write to the lcd
    
    l1 = ''#line 1
    l2 = ''#line 2 
    if(len(s)>16):
        l1=s[:16]
        l2=s[16:]
    else:
        l1=s
    lcd.backlight(1)#turn on the backlight
    lcd.lcd_clear()
    lcd.lcd_display_string(l1,1)
    lcd.lcd_display_string(l2,2)


nextPin = 6
prevPin = 12 
pausePin = 16



gp.setmode(gp.BCM)
gp.setup(nextPin,gp.IN, pull_up_down=gp.PUD_DOWN)
gp.setup(prevPin,gp.IN, pull_up_down=gp.PUD_DOWN)
gp.setup(pausePin,gp.IN, pull_up_down=gp.PUD_DOWN)

lcd = LCD.lcd()

write(lcd,"Loading Stations")
stations = []

with open(Path+sname, 'r') as f:#open the stations file
    lines = f.readlines()
    for i in lines:
        tmp = i.split(',') #its a csv file
        tmpy = (tmp[0],tmp[1].rstrip())
        stations.append(tmpy)
    f.close()

write(lcd,"Waiting For Connection")
while(True):#verify that the internet is conected properly
    internet = os.system("ping -c 1 google.com")
    if(internet == 0):
        break


start = stations[0]

print("Playing %s"%start[0])
write(lcd,start[0])
playing(start[0])

player = vlc.MediaPlayer(start[1].rstrip())
player.play()

period = time.time()
pause = False
dum = True
i=0
while(True): #TODO Implement buttons
    if(int(time.time()-period) >= 5 and dum):#clear screen every 5 seconds
        write(lcd,'')
        lcd.backlight(0)
        dum = False

    flag = True
    der  = 1#derection
    
    if(gp.input(pausePin)):
        pause = not pause
        dum = True
        player.set_pause(pause)
        tmp = stations[i][0]
        if(pause):
            write(lcd,"Paused")
            playing()
        else:
            write(lcd,tmp)#write the name
            playing(name)
        
        period = time.time()
        time.sleep(0.5)

    if(gp.input(prevPin)):
        der = -1
    elif(gp.input(nextPin) == 0):
        flag = False
    
    if(flag):
        dum = True
        i = i + der
        length = len(stations)-1
        if(i < 0):
            i = length
        elif(i > length):
            i = 0

        tmp = stations[i]
        print("Playing %s"%tmp[0])
        write(lcd,tmp[0])
        playing(tmp[0])

        player.stop()
        stat = tmp[1].rstrip()
        player = vlc.MediaPlayer(stat)
        player.play()
        period = time.time()
        time.sleep(0.5)



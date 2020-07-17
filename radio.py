#!/usr/bin/env python3
import time
import vlc
from threading import Thread
import RPi.GPIO as gp
print("HELLO")
import lcdLib as LCD
class Radio(Thread):
    Path = "/home/pi/Documents/radio/"#TODO
    sname = "stations.csv"#TODO
    
    lcState = True
    pState = True 
    
    i = 0
    period = 0.0
    stations = []
    cPlay = ""

    player = vlc.MediaPlayer()
    lcd = LCD.lcd()
    
    
    nextPin = 6
    prevPin = 12 
    pausePin = 16
    gp.setmode(gp.BCM)
    gp.setup(nextPin,gp.IN, pull_up_down=gp.PUD_DOWN)
    gp.setup(prevPin,gp.IN, pull_up_down=gp.PUD_DOWN)
    gp.setup(pausePin,gp.IN, pull_up_down=gp.PUD_DOWN)
    
    
    
    def __init__(self,i=0):
        
        Thread.__init__(self)
        print("\n\n HELLLO DOLLY \n\n")
        
        self.i = i
        self.write("Loading Stations")
        self.stations = self.statLoad()
        self.Play()
    
    def write(self, s=''):#write to the lcd
        l1 = ''#line 1
        l2 = ''#line 2
    
        if(len(s)>16):
            l1=s[:16]
            l2=s[16:]
        else:
            l1=s
        self.lcd.lcd_clear()
        self.lcd.lcd_display_string(l1,1)
        self.lcd.lcd_display_string(l2,2)
        if (s == ""):
            self.lcd.backlight(0)#turn off the backlight
            self.lcState=False
        else:
            self.lcState=True

    def Play(self, der=0, i=-1):
        if i == -1:#der specified
            self.i = self.i + der
            length = len(self.stations)-1
            if(self.i < 0):
                self.i = length
            elif(self.i > length):
                self.i = 0
        else:#specified a station
            self.i = i
        tmp = self.stations[self.i]
        self.cPlay = tmp[0]
        print("Playing %s"%self.cPlay)
        self.write(self.cPlay)
        self.period = time.time()
        try:
            self.player.stop()
            self.player = vlc.MediaPlayer(tmp[1])
            self.player.play()
            return 0
        except:
            print("ERROR PLAYING")
            return -1

    def statLoad(self):#return stations
        stations = []
        with open(self.Path+self.sname, 'r') as f:#open the stations file
            lines = f.readlines()
            for i in lines:
                tmp = i.split(',') #its a csv file
                tmpy = (tmp[0],tmp[1].rstrip())
                stations.append(tmpy)
            f.close()
        return stations

    def pause(self):
        tmp = self.stations[self.i][0]
        self.period = time.time()
        if(self.pState):
            self.write("Paused")
        else:
            self.write(tmp)#write the name
        
        temp = self.pState
        self.player.set_pause(int(temp))
        self.pState = not temp

    def run(self):
        while(True):
            if(int(time.time()-self.period) >= 5 and self.lcState):#clear screen every 5 seconds if screen is on
                self.write()
            
            flag = False
            der  = 1#derection ha ha dir is keyword
            if(gp.input(self.pausePin)):
                self.pause()
                time.sleep(0.5)
            elif(gp.input(self.prevPin)):
                der = -1
                flag = True
            elif(gp.input(self.nextPin)):
                flag = True

            if(flag):
                self.Play(der)
                time.sleep(0.5)

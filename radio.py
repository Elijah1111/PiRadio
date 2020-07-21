#!/usr/bin/env python3
import time
import vlc
from threading import Thread
import RPi.GPIO as gp
import lcdLib as LCD
class Radio(Thread):
    Path = "/home/pi/Documents/radio/"#TODO
    sname = "stations.csv"#TODO
    
    lcState = True #LCD on?
    pState = True  #Paused?

    i = 0 #The current index of the station
    period = 0.0 #The period the LCD has been on, so it can blank
    stations = [] #Stations
    cPlay = "" #What is currently playing

    player = vlc.MediaPlayer() #vlc is playing the station
    lcd = LCD.lcd() #The LCD screen
    
    
    nextPin = 6 #Pins for buttons
    prevPin = 12 
    pausePin = 16
    gp.setmode(gp.BCM)
    gp.setup(nextPin,gp.IN, pull_up_down=gp.PUD_DOWN)#Set the inputs to be pulldown
    gp.setup(prevPin,gp.IN, pull_up_down=gp.PUD_DOWN)
    gp.setup(pausePin,gp.IN, pull_up_down=gp.PUD_DOWN)
    
    
    
    def __init__(self,i=0):
        
        Thread.__init__(self)#Start the thread
        
        self.i = i #if an I is specified Defualt to 0
        self.write("Loading Stations")
        self.stations = self.statLoad()
        self.Play(i=i) #Start at whatever the index is
    
    def write(self, s=''):#write to the lcd
        
        self.lcd.lcd_clear()#Clear the Previous message if there was one
        if (s == ""):#Blank message passed
            self.lcd.backlight(0)#turn off the backlight
            self.lcState=False#LCD is off
            return 0
        else:
            self.lcState=True
        
        l1 = ''#line 1
        l2 = ''#line 2
    
        if(len(s)>16):#Split the message on to 2 lines
            l1=s[:16]
            l2=s[16:]
        else:
            l1=s
        try:
            self.lcd.lcd_display_string(l1,1) #Write the first line
            self.lcd.lcd_display_string(l2,2) #Write the second line
            return 0
        except:
            #An error has somehow happend
            print("ERROR WRITING TO SCREEN")
            return -1

    def Play(self, der=0, i=-1):
        
        if i == -1:#direction is specified, not index
            self.i = self.i + der#add the derection
            length = len(self.stations)-1
            if(self.i < 0):#flip to the end
                self.i = length
            elif(self.i > length):#flip to the front
                self.i = 0
        else:#specified a station
            self.i = i

        tmp = self.stations[self.i]
        
        self.cPlay = tmp[0]
        print("Playing %s"%self.cPlay)
        self.write(self.cPlay)
        self.period = time.time()#we updated the screen, so lets start timing it

        try:#try to play station
            self.player.stop()#stop playing if it was playing
            self.player = vlc.MediaPlayer(tmp[1])#Set to the station URL
            self.player.play()#play the station
            return 0
        except:
            print("ERROR PLAYING")
            return -1

    def statLoad(self): #Load the stations, returns a list of tuples
        stations = []
        with open(self.Path+self.sname, 'r') as f: #open the stations file
            for line in f:
                tmp = line.split(',') #its a csv file
                tmpy = (tmp[0],tmp[1].rstrip())#make a tuple, and strip off the end
                stations.append(tmpy)
            f.close()
        return stations

    def pause(self):#Pause the station
        if(self.pState):
            self.write("Paused")
        else:
            self.write(self.stations[self.i][0])#unpause write the name again
        
        self.period = time.time()#We just wrote to the screen start timing
        temp = self.pState
        self.player.set_pause(int(temp))
        self.pState = not temp


    def vol(self,vol):#Change the volume
        self.player.audio_set_volume(vol)

    def run(self):#run the radio
        while(True):
            if(self.lcState and (int(time.time())-self.period) >= 5):#clear screen every 5 seconds if screen is on
                self.write()
            
            flag = False
            der  = 1#derection, dir is keyword
            if(gp.input(self.pausePin)):
                self.pause()#pause
                time.sleep(0.5)#delay in the button
            elif(gp.input(self.prevPin)):
                der = -1
                flag = True
            elif(gp.input(self.nextPin)):
                flag = True


            if(flag):#play a diffrent staion
                self.Play(der)#play with a direction
                time.sleep(0.5)

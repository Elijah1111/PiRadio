radio.py                                                                                            0000755 0001750 0001750 00000006265 13657412365 010360  0                                                                                                    ustar   pi                              pi                                                                                                                                                                                                                     #!/usr/bin/env python3
import time
import vlc
from threading import Thread
import RPi.GPIO as gp
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

    def Play(self, der=0):
        self.i = self.i + der
        length = len(self.stations)-1
        if(self.i < 0):
            self.i = length
        elif(self.i > length):
            self.i = 0

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
                                                                                                                                                                                                                                                                                                                                           stations.csv                                                                                        0000644 0001750 0001750 00000001316 13656552563 011262  0                                                                                                    ustar   pi                              pi                                                                                                                                                                                                                     CO CPR Indie 102.3,https://stream1.cprnetwork.org/cpr3_lo
DC WPFW 89.3,http://www.wpfwfm.org:8000/wpfw_128
INDIA bouxout.FM,https://boxoutfm.out.airtime.pro/boxoutfm_a
CAN CJSF 90.1,https://www.cjsf.ca:8443/listen-hq
CO Hippie Radio 97.5,https://ice9.securenetsystems.net/KWUZFM?playSessionID=B09921A6-A4FC-6523-A1DE81BBA4239F43
MEX UNAM 96.1,http://server1.usatelk.com:27547/stream
PERU Felicidad 88.9,https://18313.live.streamtheworld.com/RADIO_FELICIDAD.mp3?DIST=RPPplayer&TGT=RPPplayer&maxServers=2&ua=RadioTime&ttag=RadioTime
JAM Joint Radio,http://radio.jointil.net:9998//;stream/1
NZ Te Hiku Radio,https://listen.tehiku.radio:8000/te_hiku_fm
RUS Nashe Radio,https://nashe1.hostingradio.ru:18000/nashe20-128.mp3
                                                                                                                                                                                                                                                                                                                  templates/                                                                                          0000755 0001750 0001750 00000000000 13657270304 010665  5                                                                                                    ustar   pi                              pi                                                                                                                                                                                                                     templates/station.html                                                                              0000644 0001750 0001750 00000001001 13657125666 013236  0                                                                                                    ustar   pi                              pi                                                                                                                                                                                                                     <!DOCTYPE html>
<html>
    <head>
	    <title>
		    PiRadio Stations
	    </title>
    </head>
    <body>
	    <center>
	    	<h1>Loaded PiStations</h1>
		
		<hr/>
		{% for i in stat %}
			<p>{{i}}</p>
		{% endfor%}
		<br/>	
		

		<p>
			DO SOMETHING ABOUT ADDING
		</p>
		
		<hr/>

		<p>
		Return to <a href="/">Home</a>
                </p>
		<hr/>
	    	<p>
	    	PiRadio is open source and avalible on <a href="https://github.com/Elijah1111/PiRadio">GitHub</a>
	    	</p>
	    </center>
    </body>
</html>

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               templates/radio.html                                                                                0000644 0001750 0001750 00000001231 13657270273 012653  0                                                                                                    ustar   pi                              pi                                                                                                                                                                                                                     <!DOCTYPE html>
<html>
    <head>
	    <title>
		    PiRadio Home
	    </title>
    </head>
    <body>
	    <center>
		<h1>PiRadio Currently Playing</h1>
		<p>{{playing}}</p>
		<p></p>
		<form action="#" method="post">
		
		<button type="submit" name="state" value="-1"> Previous</button>
		<button type="submit" name="state" value="0">Pause</button>
		<button type="submit" name="state" value="1">Next</button>
		
		</form>
		

		<p>Load More Stations <a href="./station.html">Here</a></p>
		

		<hr/>
	    	<p>
	    	PiRadio is open source and avalible on <a href="https://github.com/Elijah1111/PiRadio">GitHub</a>

	    	</p>
	    </center>
    </body>
</html>

                                                                                                                                                                                                                                                                                                                                                                       web.py                                                                                              0000755 0001750 0001750 00000001563 13657410375 010032  0                                                                                                    ustar   pi                              pi                                                                                                                                                                                                                     #!/usr/bin/python3

from flask import Flask, render_template, request
import radio as r
import threading, os

while(True):#wait for internet
    if(os.system("ping -c 1 google.com")==0):
        break

rad = r.Radio()
rad.start()



web = Flask(__name__)

@web.route("/", methods=["POST" , "GET"])
def home():
    if (request.method == "POST"):
        tmp = int(request.form["state"])
        if (tmp == -1):
            rad.Play(-1)
            print("Previous")
        elif (tmp == 0):
            rad.pause()
            print("Pause")
        elif (tmp == 1):
            rad.Play(1)
            print("Next")

    return render_template("radio.html",playing=rad.cPlay)

@web.route("/station.html")
def stations():
    return render_template("station.html",stat=rad.stations)
# run the application
if __name__ == "__main__":
    web.run(host="0.0.0.0", port="80", debug=False)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
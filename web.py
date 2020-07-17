#!/usr/bin/python3

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

@web.route("/station.html", methods=["POST","GET"])
def stations():
    if (request.method == "POST"):
        rad.Play(i=int(request.form["station"]))  
    return render_template("station.html",stat=rad.stations)
# run the application
if __name__ == "__main__":
    web.run(host="0.0.0.0", port="80", debug=False)

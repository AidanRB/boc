#!/usr/bin/env python

from flask import Flask, render_template, request, flash, redirect
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ngi787o463a64389yw563gg653wvg653536v536n89v563'

def openBoc():
    global bocf
    try:
        bocf = open("boc.txt", "r+")
    except IOError:
        bocf = open("boc.txt", "w+")

def readBoc():
    global boc
    boc = []
    for cen in bocraw:
        eventsraw = cen.split("\n")
        eventsraw.pop(0)
        events = []
        for event in eventsraw:
            if(event != ''):
                #event = event.split(".", 1)[1]
                events.append([event[6:10], event[14:]])
        boc.append(events)
    #boc[-1][-1][-1] = boc[-1][-1][-1][:-1]

def initBoc():
    bocf.write("# Book of Centuries\n\n")
    for century in range(21):
        bocf.write("## Century: " + str(century).zfill(2) + "00s:\n\n")

def getCentury(century):
    return boc[century - 1]

def getEvent(century, event):
    try:
        return boc[century - 1][event - 1]
    except:
        return False

def editEvent(century, event, year, content):
    try:
        boc[century - 1][event - 1][0] = str(century).zfill(2) + str(year)
        boc[century - 1][event - 1][1] = str(content)
        return True
    except:
        return False

def newEvent(century, year, content):
    boc[century - 1] = sorted(boc[century - 1] + [[str(century).zfill(2) + str(year), str(content)]])

def deleteEvent(century, event):
    try:
        boc[century - 1].pop(event - 1)
        return True
    except:
        return False

def getTowrite():
    towrite = "# Book of Centuries\n\n"
    cennum = 0
    for century in boc:
        towrite += "## Century: " + str(cennum).zfill(2) + "00s:\n"
        for event in century:
            towrite += "  - **" + event[0] + ":** " + event[1] + "\n"
        towrite += "\n"
        cennum += 1
    return towrite

def writeBoc():
    bocf.truncate(0)
    bocf.write(getTowrite())

@app.route("/")
def homepage():
    try:
        return render_template("boc.html", boc=zip(boc, range(len(boc))))
    except:
        return redirect("/start", code=307)

@app.route("/start")
def openpage():
    openBoc()
    global bocraw
    bocraw = bocf.read()
    bocraw = bocraw.split("\n\n## Century: ")
    bocraw.pop(0)
    if(len(bocraw) < 22):
        readBoc()
    else:
        initBoc()
    return redirect("/", code=308)

#writeBoc()
#bocf.close()

if __name__ == "__main__":
    app.run()

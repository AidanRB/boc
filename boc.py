#!/usr/bin/env python

from flask import Flask, render_template, request, flash, redirect
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ngi787o463a64389yw563gg653wvg653536v536n89v563'

phs = """Someone assasinates some other person.
The king of France... becomes the king of France.
Soandso kills Whoandsuch and becomes king of Whachamacallit.
The king of another place dies. Everone wants his throne. War, war, war!
The Prime Minister of England quits; confusion and death of many follows.
The country Brttania runs out of grass. Of course, the Europian grass-sellers make a lot of money.
One of the grass-sellers assasinates the king, takes the crown and then tries to take over the world.
All the king's horses and all of his men (him being from Egypt) decide against war of any kind and become tree-huggers.
Germany is invaded by bunnies from the Netherlands, but is able to defend her shores.
Country gets conquered! And then... conquers itself back.
The Duke of Manchester dies, and somehow that causes civil war, and somehow it leads to a world war, and bad things happen.
Political upheaval in New Jersey. No one notices.
There's an arranged marriage between two members of royalty/nobility.
The USSR decides to change its name to "International Place of Russianism", and so becomes IPR.
History repeats itself; duh, there's a war somewhere.
France is ashamed at itself for not being better than everybody else... and tries to expand her borders.
Somebody declares a war! Which accomplishes... nothing.
Some famous philosopher is killed in Greece, and only because he's smarter than everyone else.
There is an epidemic of giggles which spreads throughout Italy; it's hilarious!
The Roman Empire conquers something!
A man travels across Western Sahara as a missionary, and his adventures are published world-wide in a famous book.
The pope's dog dies.
King what's-his-name of that country over yonder goes crazy and is impeached.... that really confuses a lot of people.
The people of France riot, throwing cheerios at the king.
A seemingly insignificant short man destroys the greatest weapon known to mankind by giving it to a pale, clumsy creature.
A doctor in Norway discovers the cause of thousands of people breaking out with "Down with the king!" is a certain type of food. So the people no longer are allowed food. ...War.
A man is nailed to a tree for saying how great it would be to be nice to people for a change.
A certain commander is born, descended from the Root of All Evil.
There is an uprising in a little town in Iran, so oil prices go up.
A king decides to try to conquer the world!
There's a major depression in Switzerland because of the duck-market. Too many people buying ducks, and then a quick decline in duck-buyers.
Somebody wants to be king.
Civil war over who inherits the throne!
The President of the U.S. lives in the White House.
Two countries fight over a trade route.
A king of England kills his brother to ensure his entitlement to the throne.
A prince is murdered.
England declares war on France. Again.""".split("\n")

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
    century = int(century)
    boc[century] = sorted(boc[century] + [[str(century).zfill(2) + str(year), str(content)]])

def deleteEvent(century, event):
    try:
        boc[century].pop(event - 1)
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
    bocf.seek(0)
    bocf.write(getTowrite())

@app.route("/")
def homepage():
    try:
        return render_template("boc.html", boctosend=zip(boc, range(len(boc))), phs=phs)
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

@app.route("/add", methods=['POST'])
def addpage():
    newEvent(request.form["century"], request.form["year"], request.form["eventtext"])
    return redirect("/")

@app.route("/delete", methods=['POST'])
def removepage():
    deleteEvent(int(request.form["century"]), int(request.form["year"]))
    return redirect("/")

@app.route("/save", methods=['POST'])
def savepage():
    writeBoc()
    return redirect("/")

#writeBoc()
#bocf.close()

if __name__ == "__main__":
    app.run()

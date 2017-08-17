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
                event = event.split(".", 1)[1]
                events.append([event[4:6], event[10:]])
        boc.append(events)
    #boc[-1][-1][-1] = boc[-1][-1][-1][:-1]

def initBoc():
    bocf.write("# Book of Centuries\n\n")
    for century in range(21):
        bocf.write("## Century: " + str(century) + "00s:\n\n")

def getCentury(century):
    return boc[century - 1]

def getEvent(century, event):
    try:
        return boc[century - 1][event - 1]
    except:
        return False

def editEvent(century, event, year, content):
    try:
        boc[century - 1][event - 1][0] = str(year)
        boc[century - 1][event - 1][1] = str(content)
        return True
    except:
        return False

def newEvent(century, year, content):
    boc[century - 1] = sorted(boc[century - 1] + [[str(year), str(content)]])

def deleteEvent(century, event):
    try:
        boc[century - 1].pop(event - 1)
        return True
    except:
        return False

openBoc()
bocraw = bocf.read()
bocraw = bocraw.split("\n\n## Century: ")
bocraw.pop(0)
if(len(bocraw) < 22):
    readBoc()
else:
    initBoc()


getCentury(1)
getEvent(1, 3)
editEvent(1, 1, 46, "one")
newEvent(1, 62, "one and a half")
deleteEvent(1, 3)

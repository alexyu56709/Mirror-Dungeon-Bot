import time, pyautogui
from os import listdir
from os.path import isfile, join

from pyscreeze import Box

from UI import *
from nodePathFind import move

screenwid, screenlen = pyautogui.size()
pyautogui.FAILSAFE = False


abnopath = "ObjectDetection/abno/other/"
bodypath = "ObjectDetection/abno/body/"
EGOpath = "ObjectDetection/EGO/"

probabilities = ["VeryHigh.png", "High.png", "Normal.png", "Low.png", "VeryLow.png"]

parts = [join(abnopath, f) for f in listdir(abnopath)]
bodyparts = [join(bodypath, f) for f in listdir(bodypath)]
parts.extend(bodyparts)

banned = [f for f in listdir("blacklist/") if isfile(join("blacklist/", f))]
egoList = ["crow", "fluid", "bodysack", "regret", "wish", "star"]


def locateAll(imagefullpath, conf):
    positions = []
    threshhold = 8

    try:
        p = Box(0, 0, 0, 0)
        posit = pyautogui.locateAllOnScreen(imagefullpath, confidence=conf, grayscale=False)
        for pos in posit:
            if abs(pos[0] - p[0]) > threshhold \
            or abs(pos[1] - p[1]) > threshhold:
                positions.append(pos)
                p = pos
    finally: 
        return positions


def pause():
    window = pyautogui.getActiveWindowTitle()
    if window != 'LimbusCompany':
        while 1:
            print(     "The game is paused...\n"
                       "It seems that you have closed Limbus company window")
            do = input("Press 1 to continue or press 0 to exit: ")
            if do == "0":
                exit()
            if do == "1":
                time.sleep(8)
                break


# just heal
def shop():
    pyautogui.click(1156, 316) # heal for 100
    time.sleep(0.5)
    if pyautogui.pixelMatchesColor(1089, 500, (235, 201, 159), tolerance=10):
        pyautogui.click(1400, 500) # all heal
    else:
        pyautogui.click(1400, 677) # no heal
    time.sleep(2)
    clickonskip()
    pyautogui.click(1793, 914) # press continue
    time.sleep(0.3)
    pyautogui.click(1793, 914) # and Leave
    time.sleep(0.7)
    pyautogui.click(1144, 738) # confirm
    time.sleep(3)
    # get money from screen


# just autorest I am too lazy to look into this deeper
def rest():
    pyautogui.click(1280, 371) # we assume that we have money (not having money sucks)
    time.sleep(0.5)
    if pyautogui.pixelMatchesColor(1089, 500, (235, 201, 159), tolerance=10):
        pyautogui.click(1400, 500) # all heal
    else:
        pyautogui.click(1400, 677) # no heal
    time.sleep(2)
    clickonskip()
    pyautogui.click(1793, 914) # press continue
    time.sleep(0.3)
    pyautogui.click(1793, 914) # and Leave
    time.sleep(0.7)
    pyautogui.click(1144, 738) # confirm
    time.sleep(3)


def pthenenter():
    pyautogui.press("p", 1, .1)
    pyautogui.press("enter", 1, .1)
    time.sleep(5)
        

# this def is the def that handles simple fights with enemies.
def mainfight():
    if not UIcheck('fork.png', 0.8):
        return
    
    time.sleep(1)

    Abno = isAbno()

    pthenenter()  # first pass
    time.sleep(4)
    while 1:
        pause()
        if UIcheck('fork.png', 0.8):
            time.sleep(1)
            pyautogui.click(500, 83)

            if Abno == True:
                egoSpam()

            pthenenter()
            print("STILL FIGHTING")

        if (UIcheck('loading.png', 0.7) or 
            UIcheck('Move.png', 0.9) or 
            UIcheck('eventskip.png', 0.8)):

            print("DONE FIGHTING")
            time.sleep(8)
            return
        time.sleep(1)


def getevent() -> bool:
    time.sleep(.5)
    print("EVENT")
    if UIconfirm("TOBATTLE.png", conf=0.8):
        time.sleep(10)
        mainfight()
    else:
        if UIcheck("eventskip.png", conf=0.8):
            clickonskip()
            clickonskip()
            if UIcheck("shop.png", conf=0.8):
                print("SHOP")
                shop()
            elif UIcheck("rest.png", conf=0.8):
                print("RESTSHOP")
                rest()
            else:
                doevent()
        else:
            return False
    return True


def clickonskip():
    for i in range(3):
        pyautogui.click(903, 465)
        time.sleep(.3)


def doevent(): 
    print("EVENT")
    first = 0 
    while 1:
        match (deteventstage(0)):
            case 0: 
                print("DONE WITH EVENT")
                if first == 1:
                    break
                else:
                    clickonskip()
                    first = first + 1
            case 1: 
                dotext()
            case 2: 
                sinprob()
            case 3:
                pyautogui.click(1793, 914)


def deteventstage(ret) -> int:  # Determines what event stage we're on, 3 for possible finish, 2 for probability
    # 1 for text option selection
    if eventend():
        ret = 3
    elif UIcheck('advantage.png', 0.8):
        ret = 2
    elif UIcheck('choices.png', 0.8):
        ret = 1
    print(str(ret))
    return ret


def dotext(): 
    time.sleep(1)
    if not UIconfirm("EGOgift.png", 0.9):
        pyautogui.click(1038, 279)
    time.sleep(1)
    clickonskip()
    print("Returning")


def sinprob():
    time.sleep(2)
    for prob in probabilities:
        if UIconfirm("sinprob/" + prob, 0.75):
            break
    time.sleep(1)
    for i in range(2):
        pyautogui.click(1705, 931)
    time.sleep(5)
    clickonskip() 
    pyautogui.click(1793, 914)


def eventend() -> bool:
    if pyautogui.pixelMatchesColor(1692, 944, (160, 50, 35), tolerance=20):
        print("Done?")
        #  pyautogui.click(1793, 914)
        return True
    return False


def encounterreward() -> bool:
    try:
        pyautogui.locateOnScreen(f"{UIpath}encounterreward.png", confidence=.8)
        pyautogui.screenshot(f"choice/{int(time.time())}.png")
        time.sleep(0.7)
        pyautogui.click(869, 494)
        time.sleep(.3)
        pyautogui.click(1093, 787)
        time.sleep(0.7)
        UIconfirm("EGOconfirm.png", 0.8)
        time.sleep(5)
        return True
    except pyautogui.ImageNotFoundException:
        return False


def grabEGO() -> bool:
    print("in grabEGO")
    try:
        pyautogui.locateOnScreen(f"{UIpath}EGObin.png", region=(80, 40, 177, 143), confidence=0.9)
        print("GIFT FOUND")
        pyautogui.screenshot(f"choice/{int(time.time())}.png")
        #try: check for mounting trials
        pyautogui.click(950, 540)
        time.sleep(2)
        pyautogui.click(1700,865)
        pyautogui.click(1700,865)
        time.sleep(5)
        UIconfirm("EGOconfirm.png", 0.8)
        print("GIFT CONFIRMED")
        return True
    except pyautogui.ImageNotFoundException:
        return encounterreward() or UIconfirm("EGOconfirm.png", 0.8)


def isPack(): # def to recognize that we are in pack choice event
    print("pack choice?")
    try:
        pyautogui.locateOnScreen(f"{UIpath}PackChoice.png", region=(1733, 234, 164, 154), confidence=0.9)

        img = pyautogui.screenshot()
        img.save(f"stages/{int(time.time())}.png")

        return True
    except pyautogui.ImageNotFoundException:
        return False


def clickDrag():
    x, y = pyautogui.position()
    pyautogui.dragTo(x, y + 300, 0.5, button="left")


def blacklist(offset):
    for img in banned:
        try:
            pyautogui.locateOnScreen(f"blacklist/{img}", region=(117 + offset, 229, 407, 608), confidence=0.7)
            print(f"got {img[:-4]}")
            return True
        except pyautogui.ImageNotFoundException:
            continue
    return False
    

def PackChoice(): # def to choose the next level
    if isPack() == False:
        return
    for i in range(5): # 5 cards
        time.sleep(1)
        offset = 322 * i
        pyautogui.moveTo(416 + offset, 421)
        if i == 4:
            clickDrag()
            break
        try:
            pyautogui.locateOnScreen(f"{UIpath}warning.png", region=(228 + offset, 311, 188, 110), confidence=0.7)
            continue
        except pyautogui.ImageNotFoundException:
            if blacklist(offset) == True:
                continue
            else:
                clickDrag()
                break
    time.sleep(5)


def claimRewards():
    pyautogui.click(1667, 855)
    time.sleep(1)
    pyautogui.click(1667, 855)
    time.sleep(2)
    pyautogui.click(1274, 812)
    time.sleep(2)
    pyautogui.click(1156, 724)
    time.sleep(10)
    pyautogui.click(966, 690)
    time.sleep(10)


def locateBody():
    for part in bodyparts:
        icons = locateAll(part, 0.8)
        for icon in icons:
            x, y = pyautogui.center(icon)
            regions = [(max(0, x - 224),max(0, y - 80), 160, 160), 
                    (min(1920, x + 64), max(0, y - 80), 160, 160)]
            for i in range(2):
                try:
                    pyautogui.locateOnScreen(part, region=regions[i], confidence=0.8)
                    return True
                except pyautogui.ImageNotFoundException:
                    continue
    return False


def isAbno():
    pyautogui.moveTo(1244, 18)
    pyautogui.dragTo(883, 418, 1, button="left")
    pyautogui.moveTo(1767, 955)
    time.sleep(0.5)
    for i in range(50):
       pyautogui.scroll(1)
    time.sleep(0.5)
    print(parts)
    for part in parts:
        try:
            pyautogui.locateOnScreen(part, confidence=0.7)
            print("part located")

            pyautogui.screenshot(f"abnos/{int(time.time())}.png")

            if part[:26] == bodypath and locateBody() == False:
                raise pyautogui.ImageNotFoundException
            return True
        except pyautogui.ImageNotFoundException:
            print("part not located")
            continue
    return False


def egoSpam():
    print("ego")
    TurboSpam = False
    if UIcheck('stagger.png', 0.6, (524, 914, 762, 126)) == True:
        TurboSpam = True

    for i in range(6):
        pyautogui.moveTo(600 + 123*i, 970)
        pyautogui.mouseDown()
        time.sleep(2)
        pyautogui.mouseUp()

        for j in range(6):
            if j > 1 and TurboSpam == False:
                pyautogui.click(1719, 879)
                break

            egoname = egoList[j]

            try:
                ego = pyautogui.locateOnScreen(f"{EGOpath}{egoname}EGO.png", confidence=.7)
                clickhere(ego)
                clickhere(ego)
                pyautogui.click(1719, 879)
                break
            except pyautogui.ImageNotFoundException:
                print(f"no {egoname} ego")
                if j == 5:
                    pyautogui.click(1719, 879)
            except:
                print("some file error?")

        time.sleep(1)


def mainbot():  # the main loop for the bot
    time.sleep(7)
    error = 0
    while True:
        pause()
        UIconfirm("ServerError.png", 0.8)
        PackChoice()
        moveck = move()
        eventck = getevent()
        fightck = mainfight()
        egock = grabEGO()
        if UIcheck('victory.png', 0.9, (1035, 734, 265, 125)):
            break
        if not moveck and \
           not fightck and \
           not eventck and \
           not egock:
            error += 1
        if error > 20:
            pyautogui.screenshot(f"errors/{int(time.time())}.png")
            window = pyautogui.getActiveWindowTitle()
            if window == 'LimbusCompany':
                pyautogui.hotkey('alt', 'f4')
            exit()
    claimRewards()


def egoFirst(): # def to choose first ego, too lazy to make it more "smart"
    time.sleep(3)
    pyautogui.click(766, 667) # Charge ego
    time.sleep(1)
    pyautogui.click(1458, 396) # First and second
    pyautogui.click(1458, 547)
    time.sleep(1)
    pyautogui.click(1621, 879) # Enter

def initMirror():
    time.sleep(5)
    while True:
        pause()
        UIconfirm("Drive.png", 0.8)
        time.sleep(2)
        if UIcheck("Inferno.png", 0.8):
            pyautogui.click(671, 460) # Mirror dungeons
        time.sleep(2)
        UIconfirm("Easy.png", 0.8) # Easy mirror
        time.sleep(1)
        UIconfirm("Start.png", 0.8)
        time.sleep(1)
        UIconfirm("EGOconfirm.png", 0.8)
        egoFirst()

        time.sleep(3)
        pyautogui.click(957, 800) # Accept ego
        time.sleep(1)
        pyautogui.click(957, 800)
        time.sleep(1)
        pyautogui.click(1719, 879) # Enter
        time.sleep(3)
        break


def mirrorgrind():
    do = input("How many mirrors will you grind? ")
    do = ''.join(filter(str.isdigit, do))
    if int(do) < 1:
        print("sane choice")
        return
    print(f"Grinding {int(do)} mirrors...")
    print("Switch to Limbus Window")
    for i in range(int(do)):
        time.sleep(5)
        initMirror()
        mainbot()

if __name__ == "__main__":
    mirrorgrind()

    window = pyautogui.getActiveWindowTitle()
    if window == 'LimbusCompany':
        pyautogui.hotkey('alt', 'f4')

    exit()

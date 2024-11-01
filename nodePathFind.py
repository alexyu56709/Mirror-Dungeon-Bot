import time, pyautogui, random
from pyscreeze import Box
from UI import *


def findDanteh():
    for i in range(2):
        try:
            Danteh = pyautogui.locateOnScreen(f"{UIpath}Danteh{i}.png", confidence=0.8)
            print("Danteh found")
            x, y = pyautogui.center(Danteh)
            return x, y
        except:
            continue
    return None


def findBus():
    try:
        Bus = pyautogui.locateOnScreen(f"{UIpath}Bus.png", confidence=0.55, grayscale=False)
        print("Danteh found")
        x, y = pyautogui.center(Bus)
        return x, y
    except:
        return None


def zoom(direction) -> bool:
    for i in range(6):
        Danteh = findDanteh()
        if Danteh:
            return Danteh
        pyautogui.scroll(direction)
        time.sleep(.2)
    return None


def position(object):
    pyautogui.moveTo(object)
    pyautogui.mouseDown()
    time.sleep(0.5)
    pyautogui.moveTo(629, 430, 1, tween=pyautogui.easeInOutQuad)
    time.sleep(0.5)
    pyautogui.mouseUp()
    time.sleep(0.3)
    pyautogui.moveTo(629, 560)


def hook():
    Bus = findBus()
    if Bus is None : return False
    position(Bus)
    return True


def move(): 
    if not UIcheck('Move.png', 0.9): return False
    Dante = findDanteh()
    if Dante is None: 
        Dante = zoom(-1)
        if Dante is None and findBus(): hook()
        if Dante is None: Dante = zoom(1)
        if Dante is None: return False
    
    position(Dante)
    x = 988
    y = 179
    for i in range(3):
        try:
            pyautogui.click(x, y)  # we click on the icon
            time.sleep(1.4)
            res = pyautogui.locateOnScreen(f"{UIpath}enter.png", confidence=.8)  # if valid enter will be found
            print("entering")
            clickhere(res)
            break
        except:

            if i == 2:
                return False
            
            y = y + 297
    time.sleep(.9)
    return True
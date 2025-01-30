from utils import *

PATH = f"{UI_PATH}path/"
NODE_LIST = ["event.png", "eventSmall.png", # Order MATTERS!!!
             "risk.png",  "riskSmall.png", 
             "human.png", "humanSmall.png", 
             "focus.png", "focusSmall.png"]


def find_danteh(): # looks for high resolution Dante
    for i in range(2):
        try:
            Danteh = locateOnScreenRGBA("Danteh{i}.png", confidence=0.8, path=PATH)
            print("Danteh found")
            x, y = pyautogui.center(Danteh)
            return x, y
        except:
            continue
    return None


def find_bus(): # looks for low resolution Dante
    try:
        Bus = locateOnScreenRGBA("Bus.png", confidence=0.55, grayscale=False, path=PATH)
        print("Danteh found")
        x, y = pyautogui.center(Bus)
        return x, y
    except:
        return None


def zoom(direction):
    for i in range(6):
        Danteh = find_danteh()
        if Danteh:
            return Danteh
        pyautogui.scroll(direction)
        time.sleep(0.1)
    return None


def position(object):
    pyautogui.moveTo(object)
    pyautogui.mouseDown()
    pyautogui.moveTo(429, 480, 1, tween=pyautogui.easeInOutQuad)
    pyautogui.mouseUp()
    pyautogui.moveTo(429, 610)


def hook():
    Bus = find_bus()
    if Bus is None : return False
    position(Bus)
    return True


def move(): 
    if not check("Move.png", region=(1805, 107, 84, 86), wait=0.2, path=PATH): return False
    Dante = find_danteh()
    if Dante is None: 
        Dante = zoom(-1)
        if Dante is None and find_bus(): hook()
        if Dante is None: Dante = zoom(1)
        if Dante is None: return False
    
    position(Dante)

    for node in NODE_LIST:
        conf = 0.92
        if "event" in node:
            conf = 0.8
        
        if check(node, region=(624, 101, 282, 826), click=True, skip_wait=True, conf=conf, path=PATH):
            check("enter.png", region=(1537, 739, 310, 141), click=True, error=True, path=PATH)
            pyautogui.moveTo(1721, 999)
            time.sleep(1)

            logging.info(f"Entering {node}")
            
            return True

    pyautogui.moveTo(762, 520)
    pyautogui.click()
    check("enter.png", region=(1537, 739, 310, 141), click=True, error=True, path=PATH)
    pyautogui.moveTo(1721, 999)
    time.sleep(1)
    return True
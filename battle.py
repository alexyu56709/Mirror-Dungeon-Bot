from utils import *
from event import event

PATH = f"{UI_PATH}battle/"
SINS = [name for name in listdir(f"{PATH}sins/")]


def chain():
    res = pyautogui.center(locateOnScreenRGBA("gear.png", region=(0, 761, 548, 179), confidence=0.7, path=PATH))
    pyautogui.moveTo(res)
    pyautogui.mouseDown()
    x, y = res
    x += 75
    y -= 46
    while True:
        for sin in SINS:
            try:
                locateOnScreenRGBA(f"sins/{sin}", region=(int(x), int(y), 137, 139), confidence=0.28, grayscale=False, path=PATH)
                pyautogui.moveTo(x + 68, y + 200)
                break
            except pyautogui.ImageNotFoundException:
                continue
        else:
            pyautogui.moveTo(x + 68, y + 70)
        
        if check("gear2.png", region=(int(x + 68 + 63), int(y + 70 - 31), 171, 183), skip_wait=True, conf=0.7, path=PATH):
            pyautogui.press("enter", 1, 0.1)
            pyautogui.mouseUp()
            return
        
        x += 115


def fight():
    if not check("TOBATTLE.png", region=(1586, 820, 254, 118), click=True, wait=0.2, path=PATH) and \
       not check("battleEGO.png", region=(1525, 104, 86, 81), wait=0.2, path=PATH): return False

    print("Entered Battle")

    while check("loading.png", region=(1577, 408, 302, 91), wait=2):
            print("loading screen...")
            time.sleep(0.5)

    abno = True
    if check("battleEGO.png", region=(1525, 104, 86, 81), path=PATH) and \
       check("gear.png", region=(0, 761, 548, 179), skip_wait=True, conf=0.7, path=PATH):
        abno = False

    while True:
        if check("battleEGO.png", region=(1525, 104, 86, 81), wait=1, path=PATH):
            pyautogui.click(500, 83)

            if abno:
                pyautogui.press("p", 1, 0.1)
                pyautogui.press("enter", 1, 0.1)
            else:
                chain()

        if check(button='event/eventskip.png', region=(850, 437, 103, 52), skip_wait=True):
            event()

        if check(button='loading.png', region=(1577, 408, 302, 91), skip_wait=True) or \
            check(button='path/Move.png', region=(1805, 107, 84, 86), skip_wait=True):

            print("Battle is over")
            logging.info("Battle is over")

            return True
        
        if pyautogui.getActiveWindowTitle() != 'LimbusCompany':
            pause()

        time.sleep(1)
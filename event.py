from utils import *

PROBS = ["VeryHigh.png", "High.png", "Normal.png", "Low.png", "VeryLow.png"]
PATH = f"{UI_PATH}event/"


def event():
    if not check("eventskip.png", region=(850, 437, 103, 52), skip_wait=True, path=PATH): return False

    while True:
        pyautogui.click(906, 465)

        if check("choices.png", region=(1036, 152, 199, 77), skip_wait=True, path=PATH):
            egos = locate_all("textEGO.png", conf=0.9, region=(1031, 254, 713, 516), path=PATH)
            win = locateOnScreenRGBA("textWIN.png", conf=0.9, region=(1031, 254, 713, 516), path=PATH)
            for box in egos:
                if abs(box[1] - win[1]) > 80:
                    pyautogui.click(pyautogui.center(box))
                    break

            check("Proceed.png", region=(1539, 906, 316, 126), click=True, path=PATH)

        if check("check.png", region=(1265, 434, 430, 87), skip_wait=True, path=PATH):
            for prob in PROBS:
                if check(f"sinprob/{prob}", conf=0.75, region=(42, 876, 1427, 74), click=True, skip_wait=True, path=PATH):
                    break
            check("Commence.png", region=(1539, 906, 316, 126), click=True, path=PATH)

        if check("Continue.png", region=(1539, 906, 316, 126), skip_wait=True, click=True, path=PATH):
            return True
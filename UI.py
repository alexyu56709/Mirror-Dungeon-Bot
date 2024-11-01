import pyautogui

UIpath = "ObjectDetection/UI/"


def clickhere(res):
    selwid, sellen = pyautogui.center(res)
    pyautogui.click(selwid, sellen)


def UIcheck(image, conf, reg=(0, 0, 1920, 1080)):
    try:
        pyautogui.locateOnScreen(f"{UIpath}{image}", region=reg, confidence=conf)
        print(f"located {image[:-4]}")
        return True
    except pyautogui.ImageNotFoundException:
        return False


def UIconfirm(button, conf) -> bool:
    try:
        res = pyautogui.locateOnScreen(f"{UIpath}{button}", confidence=conf)
        clickhere(res)
        return True
    except pyautogui.ImageNotFoundException:
        return False
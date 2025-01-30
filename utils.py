import time, pyautogui, easyocr, numpy as np, cv2
from log import *
from pyscreeze import Box
from os import listdir


UI_PATH = "ObjectDetection/UI/"
DUNGEON_PATH = "ObjectDetection/dungeon/"

ocr = easyocr.Reader(['en'])


def detect_char(region=(0, 0, 1920, 1080), digit = False):
    data = np.array(pyautogui.screenshot(region=region))
    results = ocr.readtext(data, decoder='greedy')
    res = ''.join((i[1] for i in results))
    if digit:
        res = int(''.join(char for char in res if char.isdigit()))
    return res


def locateAllOnScreenRGBA(button, region=(0, 0, 1920, 1080), confidence=0.8, grayscale=True, path=UI_PATH):
    screenshot = pyautogui.screenshot(region=region)
    screenshot = np.array(screenshot)

    template = cv2.imread(path + button, cv2.IMREAD_UNCHANGED)
    x, y, _, _ = region

    b, g, r, alpha = cv2.split(template)
    mask = alpha > 0

    if grayscale:
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
        template_gray = cv2.cvtColor(cv2.merge([b, g, r]), cv2.COLOR_BGR2GRAY)
        template_gray[~mask] = 0
        result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    else:
        screenshot_rgb = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        template_rgb = cv2.merge([b, g, r])
        template_rgb[~mask] = 0
        result = cv2.matchTemplate(screenshot_rgb, template_rgb, cv2.TM_CCOEFF_NORMED)

    locations = np.where(result >= confidence)
    matches = zip(*locations[::-1])

    match_w, match_h = template.shape[1], template.shape[0]

    for match_x, match_y in matches:
        if region:
            match_x += x
            match_y += y
        yield Box(match_x, match_y, match_w, match_h)


def locateOnScreenRGBA(button, region=(0, 0, 1920, 1080), confidence=0.8, grayscale=True, path=UI_PATH):
    match = next(locateAllOnScreenRGBA(button, region, confidence, grayscale, path), None)
    
    if match is None:
        raise pyautogui.ImageNotFoundException
    
    return match


def countdown(seconds):
    for i in range(seconds, 0, -1):
        progress = (seconds - i) / seconds
        bar_length = 20
        bar = "[" + "#" * int(bar_length * progress) + "-" * (bar_length - int(bar_length * progress)) + "]"
        
        print(f"Starting in: {i} {bar}", end="\r")
        time.sleep(1)
    
    print(" " * (len(f"Starting in: {seconds} [--------------------]")), end="\r")
    print("Grinding Time!")


def locate_all(imagefullpath, conf, region=(0, 0, 1920, 1080), path=UI_PATH):
    positions = []
    threshhold = 8

    try:
        p = Box(0, 0, 0, 0)
        posit = locateAllOnScreenRGBA(imagefullpath, confidence=conf, grayscale=False, region=region, path=path)
        posit = sorted(posit, key=lambda box: box[0])
        for pos in posit:
            if abs(pos[0] - p[0]) > threshhold \
            or abs(pos[1] - p[1]) > threshhold:
                positions.append(pos)
                p = pos
    finally: 
        return positions
    

def check(button: str, path=UI_PATH, click=False, region=(0, 0, 1920, 1080), conf=0.8, skip_wait=False, wait=5, error=False):
    if skip_wait:
        wait = 0.1

    for i in range(int(wait * 10)):
        try:
            res = locateOnScreenRGBA(button, region=region, confidence=conf, path=path)
            print(f"located {button[:-4]}")

            if click:
                pyautogui.moveTo(pyautogui.center(res), duration=0.1)
                pyautogui.doubleClick(duration=0.1)
                print(f"clicked {button[:-4]}")
    
            return True
        
        except pyautogui.ImageNotFoundException:
            if not skip_wait:
                time.sleep(0.1)
    
    print(f"image {button} not found")
    if error:
        raise RuntimeError

    return False


def pause():
    while True:
        print("The game is paused...")
        do = input("Press 1 to continue or press 0 to exit: ")
        if do == "0":
            exit()
        if do == "1":
            countdown(5)
            break


def close_limbus():
    if pyautogui.getActiveWindowTitle() == 'LimbusCompany':
        pyautogui.hotkey('alt', 'f4')

    exit()
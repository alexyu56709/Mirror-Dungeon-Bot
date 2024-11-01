import time
from UI import *
from Bot import pthenenter, pause


def mainfight():
    if not UIcheck('fork.png', 0.8):
        return
    
    time.sleep(1)

    pthenenter()  # first pass
    time.sleep(4)
    while 1:
        pause()
        if UIcheck('fork.png', 0.8):
            time.sleep(1)
            pyautogui.click(500, 83)

            pthenenter()
            print("STILL FIGHTING")

        if UIcheck('loading.png', 0.7):
            print("DONE FIGHTING")
            time.sleep(8)
            return
        time.sleep(1)


def luxEXP():
    UIconfirm("Drive.png", 0.8)
    time.sleep(2)
    if UIcheck("Inferno.png", 0.8):
        pyautogui.click(671, 245)
    time.sleep(2)
    UIconfirm("EXP.png", 0.8)
    time.sleep(2)
    pyautogui.click(1664, 720)
    time.sleep(2)
    UIconfirm("TOBATTLE.png", 0.8)
    time.sleep(8)
    mainfight()
    if UIcheck("victory.png", 0.8):
        pyautogui.click(1667, 855)
        time.sleep(4)


def luxThread():
    time.sleep(4)
    UIconfirm("Thread.png", 0.8)
    time.sleep(2)
    pyautogui.click(562, 711)
    time.sleep(2)
    pyautogui.click(955, 700)
    time.sleep(2)
    UIconfirm("TOBATTLE.png", 0.8)
    time.sleep(8)
    mainfight()
    if UIcheck("victory.png", 0.8):
        pyautogui.click(1667, 855)
        time.sleep(4)


def lux():
    do = input("Start? ")
    do = ''.join(filter(str.isdigit, do))
    if int(do) == 0:
        print("Ok")
        return
    print(f"Grinding lux...")
    print("Switch to Limbus Window")
    time.sleep(6)
    luxEXP()
    for i in range(3):
        luxThread()

if __name__ == "__main__":
    lux()
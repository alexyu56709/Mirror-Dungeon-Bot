from utils import *
from battle import fight
from event import event
from pack import pack
from pathing import move
from grab import grab
from shop import shop



def dungeon_start():
    try:
        check(button="start/Drive.png", region=(1229, 896, 156, 139), click=True, error=True)
        check(button="start/MD.png", region=(528, 354, 279, 196), click=True, error=True)
        check(button="start/Start.png", region=(1473, 657, 315, 161), click=True, error=True)

        check(button="start/enterInvert.png", region=(943, 669, 382, 106), click=True, error=True)
        check(button="start/ConfirmTeam.png", region=(1593, 830, 234, 90), click=True, error=True)

        # Bonus Choice:

        if check(button="start/enterBonus.png", region=(1566, 974, 266, 89), error=True):
            time.sleep(0.1)

            pyautogui.moveTo(401, 381, duration=0.1)
            pyautogui.doubleClick()
            pyautogui.moveTo(686, 381, duration=0.1)
            pyautogui.doubleClick()
            pyautogui.moveTo(966, 381, duration=0.1)
            pyautogui.doubleClick()
            pyautogui.moveTo(1241, 381, duration=0.1)
            pyautogui.doubleClick()
            time.sleep(0.1)
    
        check(button="start/enterBonus.png", region=(1566, 974, 266, 89), click=True, error=True)
        check(button="EGOconfirm.png", region=(957, 764, 330, 90), click=True, error=True)

        # Starting EGO

        time.sleep(0.1)
        check(button="teams/Burn/BurnStart.png", region=(198, 207, 937, 682), click=True, error=True)
        time.sleep(0.1)
        pyautogui.moveTo(1239, 395, duration=0.1)
        pyautogui.doubleClick()
        time.sleep(0.1)
        pyautogui.moveTo(1239, 549, duration=0.1)
        pyautogui.doubleClick()
        pyautogui.moveTo(1624, 882, duration=0.1)
        pyautogui.doubleClick()
        time.sleep(0.1)

        check(button="EGOconfirm.png", region=(794, 745, 321, 102), click=True, error=True)
        time.sleep(0.2)
        check(button="EGOconfirm.png", region=(794, 745, 321, 102), click=True, error=True)

    except RuntimeError:
        print("Initialization error")
        logging.error("Initialization error")
        pyautogui.screenshot(f"errors/init{int(time.time())}.png") # debugging
        #close_limbus()

    print("Entering MD!")


def dungeon_end(): # to edit
    pause()
    pyautogui.click(1667, 855) # Victory screen confirm
    time.sleep(1)
    pyautogui.click(1667, 855) # Claim rewards
    time.sleep(2)
    pyautogui.click(1274, 812) # Spend enkephalin
    time.sleep(2)
    pyautogui.click(1156, 724) # Are you sure? button

    while UIconfirm("EGOconfirm.png", 0.8): # Confirming rewards
        time.sleep(2)
    time.sleep(10)


def main_loop():

    dungeon_start()

    while check(button="loading.png", region=(1577, 408, 302, 91), wait=1):
        print("loading screen...")
        time.sleep(0.5)

    error = 0
    level = 1

    while True:
        if check(button="ServerError.png", region=(651, 640, 309, 124), click=True, skip_wait=True):
            logging.error('Server error happened')

        if pyautogui.getActiveWindowTitle() != 'LimbusCompany':
            pause()
        
        if check(button="end/victory.png", region=(1478, 143, 296, 116), skip_wait=True):
            logging.info('Run Completed')
            break

        packck, level = pack(level)
        moveck = move()
        fightck = fight()
        eventck = event()
        shopck = shop(level)
        egock = grab()

        if not packck and \
           not shopck and \
           not moveck and \
           not fightck and \
           not eventck and \
           not egock:
            error += 1
        if error > 20:
            logging.error('We are stuck')
            pyautogui.screenshot(f"errors/stuck{int(time.time())}.png") # debugging
            close_limbus()

    dungeon_end()


def replay_loop():

    number = input("How many mirrors will you grind? ")
    number = int(''.join(filter(str.isdigit, number)))

    if number < 1:
        print("I respect that")
        return
    
    print(f"Grinding {number} mirrors...")
    print("Switch to Limbus Window")
    countdown(5)

    logging.info('Script started')

    for i in range(number):
        logging.info(f'Iteration {i}')
        main_loop()


if __name__ == "__main__":
    replay_loop()
    close_limbus()

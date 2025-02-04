from utils import *


PATH = f"{UI_PATH}grab/"
CARD_PATH = f"{PATH}card/"
EGO_PATH = f"{PATH}levels/"



def grab_EGO():
    if not check("EGObin.png", region=(69, 31, 123, 120), skip_wait=True, path=PATH): return False

    owned = locate_all("Owned.png", region=(0, 216, 1725, 50), path=PATH, conf=0.8)
    owned_x = [box[0] + box[2] for box in owned]

    ego = locate_all("teams/Burn/Burn.png", region=(0, 309, 1920, 110), conf=0.8)
    ego = [gui.center(coord) for coord in ego]

    remove = set()
    for x in owned_x:
        for i in range(len(ego)):
            if abs(x - ego[i][0]) < 200:
                remove.add(i)
    ego = [val for i, val in enumerate(ego) if i not in remove]

    if len(ego) == 1:
        time.sleep(0.1)
        gui.click(ego[0], duration=0.1)
    elif len(ego) > 1:
        weights = [0]*len(ego)
        for i in range(len(ego)):
            for lvl in range(4, 0, -1):
                try:
                    locateOnScreenRGBA(f"{lvl}.png", region=(ego[i][0] - 106, ego[i][1] - 101, 66, 59), confidence=0.7, grayscale=False, path=EGO_PATH)
                    weights[i] = lvl
                    break
                except gui.ImageNotFoundException:
                    continue
        index_max = max(range(len(weights)), key=weights.__getitem__)
        gui.click(ego[index_max], duration=0.1)
    else:
        for lvl in range(4, 0, -1):
            try:
                res = locateOnScreenRGBA(f"{lvl}.png", region=(0, 309, 1920, 110), confidence=0.8, grayscale=False, path=EGO_PATH)
                time.sleep(0.1)
                gui.click(gui.center(res), duration=0.1)
                break
            except gui.ImageNotFoundException:
                continue
    time.sleep(0.1)
    gui.click(1687, 870)
    check("EGOconfirm.png", region=(791, 745, 336, 104), click=True)
    return True


def grab_card():
    if not check("encounterreward.png", region=(412, 165, 771, 72), skip_wait=True, path=PATH): return False

    time.sleep(0.8)

    for i in range(1, 5):
        if check(f"{i}.png", region=(219, 283, 1531, 242), skip_wait=True, click=True, path=CARD_PATH):

            check("EGOconfirm.png", region=(1118, 754, 189, 70), click=True, error=True) # confirm card
            check("EGOconfirm.png", region=(791, 745, 336, 104), wait=1, click=True)     # confirm ego

            while check("encounterreward.png", region=(412, 165, 771, 72), skip_wait=True, path=PATH): # dangerous code
                time.sleep(0.1)
            
            return True
    else:
        return False
    

def confirm():
    if not check("EGOconfirm.png", region=(791, 745, 336, 104), skip_wait=True, click=True): return False

    gui.moveTo(965, 878)

    check("EGOconfirm.png", region=(791, 745, 336, 104), skip_wait=True, click=True)
    return True
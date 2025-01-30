from utils import *



def within_region(x, y, regions):
    for i, region in enumerate(regions):
        x1, y1, w, h = region
        if x1 < x < x1 + w and y1 < y < y1 + h:
            return i


def pack_eval(level, regions, skip):
    priority = [name for name in listdir(DUNGEON_PATH) if (f"f{level}" in name and "s" in name)]
    banned  = [name for name in listdir(DUNGEON_PATH) if (f"f{level}" in name and "b" in name)]
    print(priority)
    
    pr_coords = []
    for card in priority:
        try:
            res = pyautogui.center(locateOnScreenRGBA(f"{DUNGEON_PATH + card}", region=(161, 265, 1582, 531), confidence=0.8))
            pr_coords.append(res)
            break
        except pyautogui.ImageNotFoundException:
            continue

    if pr_coords:
        return within_region(pr_coords[0][0], pr_coords[0][1], regions)
    elif level < 3 and skip != 3:
        return None
    
    bn_coords = []
    for card in banned:
        try:
            res = pyautogui.center(locateOnScreenRGBA(f"{DUNGEON_PATH + card}", region=(161, 265, 1582, 531), confidence=0.8))
            bn_coords.append(res)
            break
        except pyautogui.ImageNotFoundException:
            continue
    
    remove = set()
    if bn_coords:
        for coord in bn_coords:
            i = within_region(coord[0], coord[1], regions)
            remove.add(i)
    filtered = [val for i, val in enumerate(regions) if i not in remove]

    ego_coords = [pyautogui.center(box) for box in locate_all(f"{UI_PATH}teams/Burn/littleBurn.png", conf=0.498)]
    weight = [0]*len(filtered)
    if ego_coords:
        for coord in ego_coords:
            i = within_region(coord[0], coord[1], filtered)
            weight[i] += 1
    index_max = max(range(len(weight)), key=weight.__getitem__)
    return regions.index(filtered[index_max])


def pack(level):
    if not check(button="pack/PackChoice.png", region=(1757, 126, 115, 116), wait=0.2):
        return (False, level)
    
    check(button="pack/hardDifficulty.png", region=(1226, 26, 257, 83), skip_wait=True, click=True)

    level = detect_char(region=(725, 151, 449, 52), digit=True)

    print(f"Entering Floor {level}")
    logging.info(f"Floor {level}")

    pyautogui.moveTo(1721, 999)
    time.sleep(0.5)

    skips = 3
    card_count = len(locate_all(f"{UI_PATH}pack/PackCard.png", 0.7))
    offset = (5 - card_count)*161
    regions = [(182 + offset + 322 * i, 280, 291, 624) for i in range(card_count)]

    print(f"{card_count} Packs")

    for skip in range(skips + 1):
        id = pack_eval(level, regions, skip)
        if id:
            region = regions[id]
            name = detect_char(region=(region[0], 657, region[2], 73))
            print(f"Entering {name}")
            logging.info(f"Pack: {name}")
            x, y = (region[0] + (region[2] // 2), region[1] + (region[3] // 2))
            pyautogui.moveTo(x, y)
            pyautogui.dragTo(x, y + 300, 0.5, button="left")
            break
        if skip != 3:
            check(button="pack/refresh.png", region=(1493, 26, 257, 83), wait=1, click=True)
            pyautogui.moveTo(1721, 999)
            time.sleep(3)
    
    check(button="Move.png", region=(1805, 107, 84, 86), error=True)
    time.sleep(0.5)
    return (True, level)
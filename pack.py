from utils import *


PATH = f"{UI_PATH}pack/"



def within_region(x, y, regions):
    for i, region in enumerate(regions):
        x1, y1, w, h = region
        if x1 < x < x1 + w and y1 < y < y1 + h:
            return i


def pack_eval(level, regions, skip):
    
    if level == 1: priority = ["Outcast", "Gamblers"]
    elif level == 2: priority = ["Chicken"]
    else: priority = []

    banned = ["Factory", "Unloving", "Faith", "Crushed", "Violet", "Express", "Bullet", "Pride"]

    pr_coords = []
    data = np.array(gui.screenshot(region=(161, 657, 1582, 73)))
    results = ocr.readtext(data, decoder='greedy')

    for card in priority:
        for result in results:
            if card in result[1]:
                pr_coords.append(gui.center(Box(min(x:= [p[0] for p in result[0]]) + 161, min(y:= [p[1] for p in result[0]]) + 657, max(x) - min(x), max(y) - min(y))))
                break
        
    if pr_coords:
        return within_region(pr_coords[0][0], pr_coords[0][1], regions)
    elif level < 3 and skip != 3:
        return None
    
    bn_coords = []
    for card in banned:
        for result in results:
            if card in result[1]:
                bn_coords.append(gui.center(Box(min(x:= [p[0] for p in result[0]]) + 161, min(y:= [p[1] for p in result[0]]) + 657, max(x) - min(x), max(y) - min(y))))
    
    remove = set()
    if bn_coords:
        for coord in bn_coords:
            i = within_region(coord[0], coord[1], regions)
            remove.add(i)
    filtered = [val for i, val in enumerate(regions) if i not in remove]

    ego_coords = [gui.center(box) for box in locate_all("teams/Burn/littleBurn.png", conf=0.8)]
    owned_x = [box[0] + box[2] for box in locate_all("OwnedSmall.png", conf=0.8, path=PATH)]

    remove = set()
    for x in owned_x:
        for i in range(len(ego_coords)):
            if abs(x - ego_coords[i][0]) < 25:
                remove.add(i)
    ego_coords = [val for i, val in enumerate(ego_coords) if i not in remove]

    # print(len(ego_coords)) # testing

    weight = [0]*len(filtered)
    if ego_coords:
        for coord in ego_coords:
            i = within_region(coord[0], coord[1], filtered)
            if i == None : continue
            weight[i] += 1
    index_max = max(range(len(weight)), key=weight.__getitem__)
    return regions.index(filtered[index_max])


def pack(level):
    if not check("PackChoice.png", region=(1757, 126, 115, 116), wait=0.2, path=PATH):
        return (False, level)
    
    if check("hardDifficulty.png", region=(893, 207, 115, 44), skip_wait=True, path=PATH):
        gui.moveTo(1349, 64)
        gui.click()

    level = detect_char(region=(725, 151, 449, 52), digit=True)

    print(f"Entering Floor {level}")
    logging.info(f"Floor {level}")

    gui.moveTo(1721, 999)
    time.sleep(0.4)

    skips = 3
    card_count = len(locate_all("PackCard.png", 0.7, path=PATH))
    offset = (5 - card_count)*161
    regions = [(182 + offset + 322 * i, 280, 291, 624) for i in range(card_count)]

    print(f"{card_count} Packs")

    for skip in range(skips + 1):
        id = pack_eval(level, regions, skip)
        #gui.screenshot(f"choice/pack{int(time.time())}.png") # debugging
        if not id is None:
            region = regions[id]
            name = detect_char(region=(region[0], 657, region[2], 73))
            print(f"Entering {name}")
            logging.info(f"Pack: {name}")
            x, y = (region[0] + (region[2] // 2), region[1] + (region[3] // 2))
            gui.moveTo(x, y)
            gui.dragTo(x, y + 300, 0.5, button="left")
            break
        if skip != 3:
            check("refresh.png", region=(1493, 26, 257, 83), wait=1, click=True, path=PATH)
            gui.moveTo(1721, 999)
            time.sleep(2)
    
    if check(button="path/Move.png", region=(1805, 107, 84, 86), error=True) and level != 1:
        while check(button="path/Move.png", skip_wait=True, region=(1805, 107, 84, 86)): # potentially dangerous
            time.sleep(0.1)
        check(button="path/Move.png", region=(1805, 107, 84, 86), error=True)
    time.sleep(0.5)
    return (True, level)
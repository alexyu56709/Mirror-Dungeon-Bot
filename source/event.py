from source.utils.utils import *

PROBS = ["VeryHigh", "High", "Normal", "Low", "VeryLow"]


def event():
    if not now.button("eventskip"): return False

    start_time = time.time()
    while True:
        if time.time() - start_time > 100: return False
        if gui.getActiveWindowTitle() != 'LimbusCompany':
            pause()

        for _ in range(3): win_click(906, 465, delay=0.01)
        
        if now.button("choices"):
            time.sleep(0.1)
            #Hard coded chicken event
            nothing_boxes = LocateGray.locate_all(PTH["Nothing2"], region=REG["textEGO"])
            if nothing_boxes:
                win_click(gui.center(nothing_boxes[0]))
                print("Hard coded ckn event")
                logging.info("Hard coded ckn event")
                continue
            #Hard coded Bizarre Machine event2
            nothing_boxes = LocateGray.locate_all(PTH["Coin2"], region=REG["textEGO"])
            if nothing_boxes:
                win_click(gui.center(nothing_boxes[0]))
                print("Hard coded Bizarre Machine event2")
                logging.info("Hard coded Bizarre Machine event2")
                continue
            #Hard coded Bizarre Machine event
            nothing_boxes = LocateGray.locate_all(PTH["Coin"], region=REG["textEGO"])
            if nothing_boxes:
                win_click(gui.center(nothing_boxes[0]))
                print("Hard coded Bizarre Machine event")
                logging.info("Hard coded Bizarre Machine event")
                continue
            egos = LocateGray.locate_all(PTH["textEGO"], region=REG["textEGO"], conf=0.85)
            #print(egos)
            if not egos:
                choice = random.choice([316, 520])
                win_click(1348, choice, delay=0)
                continue
            try:
                win = LocateGray.try_locate(PTH["textWIN"], region=REG["textEGO"], conf=0.85)
                for box in egos:
                    if abs(box[1] - win[1]) > 80:
                        win_click(gui.center(box), delay=0)
                        break
                else:
                    win_click(1356, 498, delay=0)
            except gui.ImageNotFoundException:
                win_click(gui.center(egos[0]), delay=0)

        now_click.button("Proceed")

        if now.button("check"):
            matches = {
                prob: now.button(prob, "probs")
                for prob in PROBS
            }
            if any(matches.values()):
                for prob in PROBS:
                    if now_click.button(prob, "probs"):
                        click.button("Commence")
                        break

        if now_click.button("Continue"):
            connection()
            return True
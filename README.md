# ChargeGrinder
**ChargeGrinder** is a Limbus Company bot that charges through MD5 for you

### Features:
- **CURRENT VERSION IS NOT FINISHED (will update shortly)**
- **Automated Mirror Dungeon Runs:** ChargeGrinder will automatically complete all floors of the Mirror Dungeon.
- **User Input:** The program will prompt you to enter the number of Mirror Dungeons to grind, and it will start running a few seconds after your response (You must switch to Limbus Company window).
- **In-Game Requirements:** 
    - You must leave the Limbus Company window open and in fullscreen mode while the bot runs. Mouse interactions in the game will be controlled by the bot.
    - If you close the Limbus Company window, the bot will automatically pause.
- **The bot:**
    - Uses default (burn) team
    - Tries to find the best next node
    - Selects Burn Ego gifts
    - Winrates focused encounters and spams EGO on abnormalities (It only knows a few egos for now)
    - Also bot avoids a few Booster Packs with difficult fights (Dongbaek, Crabking, Casseti, Kim, Timekilling time and Ordeal of Violet Noon)
- **Limitations:** ChargeGrinder still needs additional features, testing, and bug fixes. However, it can successfully grind a few easy dungeons while you are sleeping.

---

### Requirements:
- Python 3
- `os`
- `time`
- `numpy`
- `cv2`
- `pyscreeze`
- `pyautogui`
- `easyocr`
- `logging`
---

### Setup Instructions:

1. **Team Setup:** 
   - ChargeGrinder is currently tested with an Uptie 4 burn team (the fastest option)
   - Team members: Faust, Ishmael, Gregor, Sinclair, Ryoshu and Rodion
   ![team.png](team.png)
   - The team is inspired by this MD5 speedrun:
   [![Watch on YouTube](https://img.youtube.com/vi/dCUUHMLDWkY/0.jpg)](https://www.youtube.com/watch?v=dCUUHMLDWkY)

2. **Game Settings:**
   - Set the game resolution to Full HD (1920 x 1080) in fullscreen mode.
   - Start the bot and immediately switch to Limbus window on the main game screen.
   - Also, if you have multiple languages in keyboard layout, make sure you have ENG selected before starting the bot

3. **Recommended Team:** 
   - Currently, only burn team is tested.
   - Ensure the team and all 6 sinners are selected before starting the bot. The game usually remembers previously used sinners.

---

### TODO List:
- Add support for different team builds??? idk why though if burn is the fastest
- Implement more natural mouse movements for the bot? game doesn't really track mouse movements though
- Improve abnormality fights (coin targeting instead of winrate)
- Create a bot UI using PyQt6

# -*- coding: utf-8 -*-
"""
Created on Sun May 24 10:34:01 2020

@author: jesse
"""

import tools
import enemy
import player
import items
import copy


def enterDungeon(dungeon, curRoomID):
    dungeonCopy = copy.deepcopy(dungeon)

    # input(dungeonCopy)

    while curRoomID != "L":
        localeName = dungeonCopy["name"] + " - "
        optionsList = []
        allOptions = ['a', 'w', 's', 'd']
        directionalOptions = ["left", "upward", "downward", "right"]
        keys = ["A", "W", "S", "D"]
        roomIDnum = 0

        tools.clear()

        if player.TheHero["position"] == player.TheHero["lostItems"]["position"]:
            player.reclaimLostItems()

        # Setup room options
        for idx, rooms in enumerate(dungeonCopy["rooms"]):
            if rooms["name"] == curRoomID:
                roomIDnum = idx

        optionsList.append(dungeonCopy["rooms"][roomIDnum].get("left"))
        optionsList.append(dungeonCopy["rooms"][roomIDnum].get("upward"))
        optionsList.append(dungeonCopy["rooms"][roomIDnum].get("downward"))
        optionsList.append(dungeonCopy["rooms"][roomIDnum].get("right"))

        # Handle enemy encounter
        if dungeonCopy["rooms"][roomIDnum].get("enemy"):
            enemyType = eval(dungeonCopy["rooms"][roomIDnum]["enemy"])
        else:
            enemyType = None
        enemyCount = dungeonCopy["rooms"][roomIDnum].get("enemyCount")

        if enemyType is not None and enemyCount is None:
            enemyCount = 1

        if enemyType is not None:
            for x in range(enemyCount):
                if enemy.encounter(enemyType) == False:
                    return "L"

            dungeonCopy["rooms"][roomIDnum]["enemy"] = None

            if curRoomID == "TE":
                dungeon["bossDefeated"] = True
                del dungeon["rooms"][roomIDnum]["enemy"]
                eval(dungeonCopy["rooms"][roomIDnum]["ending"])

        if dungeonCopy.get("uponEntry"):
            if eval(dungeonCopy["uponEntry"]) == False:
                return 'L'

        # Need this additional clear in case there is an enemy encounter
        tools.clear()

        # Display dungeon info
        if curRoomID[0] == "C":
            localeName += "Chamber" + " " + curRoomID[1]
            if len(curRoomID) > 2:
                localeName += curRoomID[2]
        elif curRoomID[0] == "E":
            localeName += "Entrance"
        elif curRoomID[0] == "D":
            localeName += "Dead end"

        if curRoomID != "TE":
            print("\n\n\n {" + localeName + "}", end="\n")
        else:
            print("\n\n\n {" + localeName + "Final Room}", end="\n")

        player.displayPlayerInfo()

        print("\n" * 16 + "  ", end="")

        if dungeonCopy["rooms"][roomIDnum].get("tags"):
            if dungeonCopy["rooms"][roomIDnum]["tags"].get("trapdoor") or dungeonCopy["rooms"][roomIDnum]["tags"].get("enchanted wall"):
                allOptions += 'i'


        loot = dungeonCopy["rooms"][roomIDnum].get("loot")
        if loot is not None:
            allOptions += 'p'
            print("[P]lunder chest", end="")

        if curRoomID == "E":
            allOptions += 'l'
            print("[L]eave " + dungeonCopy["name"].lower(), end="")

        print("\n   ",end="")


        tools.roomOutput(dungeonCopy, roomIDnum, optionsList, keys, directionalOptions)

        # Acquire and process player input
        selected = player.playerOptions(allOptions)

        if not selected:
            continue
        elif selected == "a":
            selected = 0
        elif selected == "w":
            selected = 1
        elif selected == "s":
            selected = 2
        elif selected == "d":
            selected = 3

        if type(selected) is int:
            if optionsList[selected] is not None:
                # input("Changing room now!")
                curRoomID = optionsList[selected]

                tools.processTagFunction(dungeonCopy, roomIDnum, curRoomID)

                player.TheHero["position"]["subLocation"] = curRoomID
                tools.gameTick()
            else:
                tools.inputIndent("Invalid selection...")

        if selected == "l" and curRoomID == "E":
            return "L"

        elif selected == "modify":
            modifyDungeon(dungeonCopy)

        elif selected == 'i':
            if dungeonCopy["rooms"][roomIDnum]["tags"].get("trapdoor"):
                tools.inputIndent("The trapdoor seems to only open one way.")
            elif dungeonCopy["rooms"][roomIDnum]["tags"].get("enchanted wall"):
                tools.inputIndent("The ornately carved wall seems to produce a gentle hum.")

        elif selected == "p" and loot is not None:
            player.plunderChest(loot)
            dungeonCopy["rooms"][roomIDnum]["loot"] = None
            del dungeon["rooms"][roomIDnum]["loot"]


def caveOfDarkVictory():
    CaveOfDark["bossDefeated"] = True
    tools.clear()
    tools.inputIndent("You have conquered the Cave of Dark!", 30, 10)
    player.TheHero["inventory"]["gold"] += 1000
    player.acquireItem(items.freshCherryPie)
    player.acquireItem(items.ultraHealthPotion)
    # player.acquireItem(items.potionOfAscendance)
    tools.clear()


def modifyDungeon(dungeon):

    if dungeon["name"] == "The Sunken Citadel":
        dungeon["rooms"][2] = {"name": "C2", "right": "C28", "downward": "C1", "left": "C3"}
        dungeon["rooms"][18] = {"name": "C18", "upward": "C17", "downward": "C19", "left": "C28"}


CaveOfDark = {
    "name": "The Cave of Dark",
    "bossDefeated": False,
    "rooms": [
        {"name": "E", "left": "D1", "upward": "C1"},
        {"name": "D1", "right": "E", "enemy": "enemy.FeralVole"},
        {"name": "C1", "left": "D2", "downward": "E", "right": "C2"},
        {"name": "D2", "right": "C1", "enemy": "enemy.Goblin"},
        {"name": "C2", "left": "C1", "upward": "C3", "enemy": "enemy.FeralVole"},
        {"name": "C3", "left": "C4", "upward": "D4", "downward": "C2", "right": "D3"},
        {"name": "C4", "upward": "TE", "right": "C3", "enemy": "enemy.Goblin", "enemyCount": 2},
        {"name": "TE", "downward": "C4", "enemy": "enemy.GoblinChieftain", "ending": "caveOfDarkVictory()"},
        {"name": "D3", "left": "C3", "loot": "small"},
        {"name": "D4", "downward": "C3", "enemy": "enemy.Goblin"},
    ]
}


def displayCaveOfDarkMap():
    tools.clear()

    spacing = 50

    tools.printIndent(" _________________",spacing,10)
    tools.printIndent("|                 |", spacing)
    tools.printIndent("|      O   O      |", spacing)
    tools.printIndent("|      |   |      |", spacing)
    tools.printIndent("|      O---O---O  |", spacing)
    tools.printIndent("|          |      |", spacing)
    tools.printIndent("|  O---O---O      |", spacing)
    tools.printIndent("|      |          |", spacing)
    tools.printIndent("|  O---E          |", spacing)
    tools.printIndent("|_________________|", spacing)

    tools.inputIndent("[Enter] to stow map",numSpaces=4,numNewLinesBefore=7)


SunkenCitadel = {
    "name": "The Sunken Citadel",
    "uponEntry": "enemy.getSpectralSandwormLocation()",
    "uponExit": "enemy.restoreSandwormState()",
    "bossDefeated": False,
    "passageRevealed": False,
    "rooms": [
        {"name": "E", "right": "C22", "left": "C1", "tags": {"dropdown": ["C22", "C1"], "trapdoor": ["downward", "upward"]}},
        {"name": "C1", "upward": "C2"},
        {"name": "C2", "downward": "C1", "left": "C3", "tags": {"enchanted wall": ["right"]}},
        {"name": "C3", "right": "C2", "upward": "C4", "enemy": "enemy.UndeadWarrior"},
        {"name": "C4", "downward": "C3", "left": "C5", "upward": "C7"},
        {"name": "C5", "right": "C4", "upward": "C6", "downward": "D2"},
        {"name": "C6", "right": "C7", "upward": "C8", "downward": "C5"},
        {"name": "C7", "downward": "C4", "left": "C6", "enemy": "enemy.JuvenileBasilisk"},
        {"name": "C8", "right": "C9", "downward": "C6", "left": "D4"},
        {"name": "C9", "right": "C10", "left": "C8", "enemy": "enemy.UndeadWarrior"},
        {"name": "C10", "right": "C15", "downward": "C11", "left": "C9"},
        {"name": "C11", "right": "C12", "upward": "C10", "left": "D3", "tags": {"dropdown": ["C12"]}},
        {"name": "C12", "upward": "C15", "downward": "C13", "tags": {"dropdown": ["C13"], "climb": ["C15"]}},
        {"name": "C13", "left": "C14", "tags": {"dropdown": ["C14"]}, "enemy": "enemy.UndeadWarrior", "enemyCount": 2},
        {"name": "C14", "downward": "TE", "tags": {"dropdown": ["TE"]}, "enemy": "enemy.JuvenileBasilisk"},
        {"name": "C15", "right": "C16", "left": "C10", "tags": {"trapdoor": ["downward"]}, "enemy": "enemy.UndeadWarrior"},
        {"name": "C16", "downward": "C17", "left": "C15"},
        {"name": "C17", "right": "D5", "upward": "C16", "downward": "C18", "enemy": "enemy.JuvenileBasilisk"},
        {"name": "C18", "upward": "C17", "downward": "C19", "tags": {"enchanted wall": ["left"]}},
        {"name": "C19", "right": "D6", "upward": "C18", "downward": "C20"},
        {"name": "C20", "upward": "C19", "left": "C21", "enemy": "enemy.JuvenileBasilisk"},
        {"name": "C21", "right": "C20", "upward": "C22", "downward": "C23"},
        {"name": "C22", "downward": "C21", "enemy": "enemy.UndeadWarrior"},
        {"name": "C23", "upward": "C21", "left": "C24", "enemy": "enemy.UndeadWarrior"},
        {"name": "C24", "right": "C23", "downward": "D7", "left": "C25"},
        {"name": "C25", "right": "C24", "upward": "C26"},
        {"name": "C26", "right": "C27", "upward": "D1", "downward": "C25", "enemy": "enemy.JuvenileBasilisk"},
        {"name": "C27", "upward": "E", "left": "C26", "tags": {"climb": ["E"]}},
        {"name": "C28", "left": "C2", "right": "C18", "enemy": "enemy.Golem", "loot": "large"},
        {"name": "D1", "downward": "C26", "loot": "medium"},
        {"name": "D2", "upward": "C5"},
        {"name": "D3", "right": "C11", "loot": "small", "enemy": "enemy.JuvenileBasilisk"},
        {"name": "D4", "right": "C8", "enemy": "enemy.UndeadWarrior"},
        {"name": "D5", "left": "C17"},
        {"name": "D6", "left": "C19", "enemy": "enemy.JuvenileBasilisk"},
        {"name": "D7", "upward": "C24", "enemy": "enemy.JuvenileBasilisk", "enemyCount": 2, "loot": "small"},
        {"name": "TR1", "right": "TE"},
        {"name": "TR2", "left": "TE"},
        {"name": "TE", "right": "TR2", "downward": "E", "left": "TR1", "tags": {"climb": ["E"]}},
    ]
}


def displaySunkenCitadelMap():
    tools.clear()

    spacing = 50

    tools.printIndent(" _________________________________",spacing, 5)
    tools.printIndent("|                                 |", spacing)
    tools.printIndent("|  O---O-----O-----O---O---O      |", spacing)
    tools.printIndent("|      |           |   |   |      |", spacing)
    tools.printIndent("|      |       O---O---O   |      |", spacing)
    tools.printIndent("|      O---O           |   |      |", spacing)
    tools.printIndent("|      |   |       O---O   O---O  |", spacing)
    tools.printIndent("|      O---O       |       |      |", spacing)
    tools.printIndent("|      |   |   O---O---O   |      |", spacing)
    tools.printIndent("|      O   |       |       |      |", spacing)
    tools.printIndent("|          O---O   |       O      |", spacing)
    tools.printIndent("|              |   |       |      |", spacing)
    tools.printIndent("|          O   O---E---O   O---O  |", spacing)
    tools.printIndent("|          |       |   |   |      |", spacing)
    tools.printIndent("|          O-------O   O---O      |", spacing)
    tools.printIndent("|          |           |          |", spacing)
    tools.printIndent("|          O-----O-----O          |", spacing)
    tools.printIndent("|_________________________________|", spacing)

    tools.inputIndent("[Enter] to stow map",numSpaces=4,numNewLinesBefore=4)

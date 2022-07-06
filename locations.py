# -*- coding: utf-8 -*-
"""
Created on Fri May  8 02:07:58 2020

@author: jesse
"""

from time import sleep
from tools import clear
from tools import saveInfo
from tools import searchList
from tools import inputIndent
from tools import gameTick
from enemy import encounter
import random
import player
import dungeons
import enemy

import npc

Tavern = {
    "name": "The Tavern",
    "action": "Enter",
    "Proceed": "enterTavern()"
}

TheGreatWiltingTree = {
    "name": "The Great Wilting Tree",
    "action": "Climb",
    "Proceed": "climbTheGreatWiltingTree()"
}

TheAbyss = {
    "name": "The Abyss",
    "action": "Fall into",
    "Proceed": "fallIntoAbyss()"
}

CaveOfAscendancy = {
    "name": "Cave Of Ascendancy",
    "action": "Enter",
    "Proceed": "player.searchChest('')"
}

TheJaggedLands = {
    "name": "The Jagged Lands",
    "subLocations": {
        "West": [
            ["Venture", "east", "Central"],
            # ["Proceed", "CaveOfAscendancy"],
        ],
        "North": [
            ["Travel", "north", "ThePlains", "Central"],
            ["Venture", "south", "Central"],
        ],
        "Central": [
            ["Venture", "west", "West"],
            ["Venture", "north", "North"],
            ["Venture", "south", "South"],
            ["Venture", "east", "East"],
            # ["Provoke", "the shadow man"],
        ],
        "South": [
            ["Venture", "north", "Central"],
            ["Approach", "npc.Shaymus"],
        ],
        "East": [
            ["Venture", "west", "Central"],
            ["Proceed", "TheAbyss"],
        ],
    },
    "enemies": [enemy.Null],  # is a list in the case that area would have multiple enemy types
}

Town = {
    "name": "Town",
    "subLocations": {
        "West": [
            ["Venture", "east", "Central"],
            # ["Provoke", "the shadow man"],
        ],
        "North": [
            ["Venture", "south", "Central"],
            ["Venture", "east", "Northeast"],
            ["Approach", "npc.TheShopkeep"],
        ],
        "Central": [
            ["Venture", "west", "West"],
            ["Venture", "north", "North"],
            ["Venture", "south", "South"],
            # ["Provoke", "the shadow man"],
        ],
        "South": [
            ["Venture", "north", "Central"],
            ["Proceed", "Tavern", "input('Entered the tavern')"],
            ["Approach", "npc.TheShadowMan"],
            # ["Provoke", "the shadow man"],
        ],
        "Northeast": [
            ["Venture", "west", "North"],
            ["Travel", "east", "ThePlains", "Central"],
            # ["Provoke", "the shadow man"],
        ]
    },
    "enemies": [enemy.Null]  # is a list in the case that area would have multiple enemy types
}

ThePlains = {
    "name": "The Plains",
    "subLocations": {
        "Central": [
            ["Travel", "west", "Town", "Northeast"],
            ["Travel", "south", "TheJaggedLands", "North"],
            ["Travel", "east", "TheWilderness", "Central"],
            # ["Provoke", "the shadow man"],
        ],
    },
    "enemies": [enemy.Null]
}

TheWilderness = {
    "name": "The Wilderness",
    "subLocations": {
        "Central": [
            ["Travel", "west", "ThePlains", "Central"],
            ["Travel", "east", "TheMarsh", "West"],
            # ["Provoke", "the shadow man"],
        ],
    },
    "enemies": [enemy.Brownie]
}

TheMarsh = {
    "name": "The Marsh",
    "subLocations": {
        "West": [
            ["Travel", "west", "TheWilderness", "Central"],
            ["Venture", "east", "Central"],
            # ["Provoke", "the shadow man"],
        ],
        "Central": [
            ["Venture", "west", "West"],
            ["Venture", "east", "East"],
            ["EnterDungeon", "dungeons.CaveOfDark"],
        ],
        "East": [
            ["Venture", "west", "Central"],
            ["Travel", "east", "Blighteth", "Central"],
            ["Proceed", "TheGreatWiltingTree"],
        ],
    },
    "enemies": [enemy.Brownie]
}

Blighteth = {
    "name": "Blighteth",
    "subLocations": {
        "Central": [
            ["Travel", "west", "TheMarsh", "East"],
            # ["Travel", "east", "TheDeep", "Central"],
            ["EnterDungeon", "dungeons.SunkenCitadel"],
        ],
    },
    "enemies": [enemy.Goblin]
}

TheDeep = {
    "name": "The Deep",
    "subLocations": {
        "Central": [
            ["Proceed", "TheAbyss"],
        ],
    },
    "enemies": [enemy.Null]
}


def processAreaOptions():
    optionsList = [None, None, None, None]
    allOptions = ['a', 'w', 's', 'd']
    directionalOptions = ["west", "north", "south", "east"]
    directionPtr = 0
    count = 0

    # First, verify that player 'location' is a cardinal location of the greater area.
    #   If not, reset player location and sublocation
    try:
        if eval(player.TheHero["position"]["location"]).get("subLocations") is None:
            player.TheHero["position"]["location"] = "Central"
            player.TheHero["position"]["subLocation"] = None
    except:
        pass

    currentArea = eval(player.TheHero["position"]["area"])
    currentLocationName = player.TheHero["position"]["location"]
    currentLocationDetails = currentArea["subLocations"][currentLocationName]

    clear()

    if player.TheHero["position"] == player.TheHero["lostItems"]["position"]:
        player.reclaimLostItems()

    print("\n\n\n {" + currentArea["name"], end="")

    if player.TheHero["position"]["location"] == "Central":
        print("}")
    else:
        print(" - " + player.TheHero["position"]["location"] + "}")

    player.displayPlayerInfo()

    # Loop as many times as needed for directionPtr to reach 4, but as soon as end of list is reached
    while directionPtr < 4:

        # Continue if the number of options in the list is greater than the value of directionPtr
        if len(currentLocationDetails) > directionPtr:

            # If index #1 of currentLocationDetails[directionPtr] is not a direction, break
            if searchList(currentLocationDetails[directionPtr][1], directionalOptions) is False:
                break

            # If the direction being searched for is found, add the option containing that direction to optionsList
            elif searchList(directionalOptions[count], currentLocationDetails[directionPtr]):
                optionsList[count] = currentLocationDetails[directionPtr]
                directionPtr += 1
            count += 1
        else:
            break

    for x, item in enumerate(currentLocationDetails[directionPtr:]):
        optionsList.append(item)
        allOptions += str(x+1)

    displayAreaOptions(optionsList)

    if getAreaInput(optionsList, allOptions) == "main":
        return False
    else:
        saveInfo()
        return True


def displayAreaOptions(optionsList):
    numOptions = len(optionsList) - 4

    print("\n" * 16, end="  ")

    i = 0
    while numOptions > i:
        if optionsList[i + 4] is not None:
            print("[" + str(i + 1) + "] ", end="")
            if optionsList[i + 4][0] == "Approach":
                print("Talk to " + eval(optionsList[i + 4][1])["name"], end="")

            elif optionsList[i + 4][0] == "EnterDungeon":
                print("Enter " + eval(optionsList[i + 4][1])["name"], end="")

            elif optionsList[i + 4][0] == "Proceed":
                locale = eval(optionsList[i + 4][1])
                print(locale["action"] + " " + locale["name"], end="")

            elif optionsList[i + 4][0] == "Provoke":
                print("placeholder", end="")

            if numOptions - 1 > i:
                print(" | ", end="")

        i += 1

    print("\n", end=" " * 3)

    for idx, item in enumerate(optionsList):

        if idx < 4:
            if item is not None:
                if optionsList[idx][1] == "west":
                    print("[A] ", end="")
                elif optionsList[idx][1] == "north":
                    print("[W] ", end="")
                elif optionsList[idx][1] == "south":
                    print("[S] ", end="")
                elif optionsList[idx][1] == "east":
                    print("[D] ", end="")

                if item[0] == "Travel":
                    print(item[0] + " " + item[1] + " to " + eval(item[2])["name"], end="")

                elif item[0] == "Venture":
                    print("Venture " + item[1], end="")

                if idx < 3 and optionsList[idx + 1] is not None:
                    print(" | ", end="")

            else:
                print(" ... " * 4, end="")


def getAreaInput(optionsList, allOptions):
    selected = player.playerOptions(allOptions)

    if not selected:
        return False
    elif selected == "a":
        selected = 0
    elif selected == "w":
        selected = 1
    elif selected == "s":
        selected = 2
    elif selected == "d":
        selected = 3
    elif selected == "main":
        return "main"
    else:
        if selected == True:
            return True
        selected = int(selected)
        selected += 3

    if selected < len(optionsList):
        if optionsList[selected] is None:
            inputIndent("Invalid selection...")

        elif optionsList[selected][0] == "Travel":
            upcomingArea = optionsList[selected][2]
            travel(eval(upcomingArea)["enemies"][0])
            player.TheHero["position"]["area"] = upcomingArea
            player.TheHero["position"]["location"] = optionsList[selected][3]
            gameTick()

        elif optionsList[selected][0] == "Approach":
            character = eval(optionsList[selected][1])
            eval(character["approach"])

        elif optionsList[selected][0] == "EnterDungeon":
            player.TheHero["position"]["location"] = optionsList[selected][1]
            player.TheHero["position"]["subLocation"] = "E"
            gameTick()
            dungeon = eval(optionsList[selected][1])
            dungeons.enterDungeon(dungeon, "E")
            if dungeon.get("uponExit"):
                eval(dungeon["uponExit"])
            gameTick()

        elif optionsList[selected][0] == "Proceed":
            pointOfInterest = eval(optionsList[selected][1])
            eval(pointOfInterest["Proceed"])

        elif optionsList[selected][0] == "Venture":
            player.TheHero["position"]["location"] = optionsList[selected][2]
            gameTick()
    else:
        input("  Invalid selection...")


def travel(enemyType):
    progression = " " * 46 + "Traveling: " + "o "
    travelSpeed = 0.15

    clear()

    if player.TheHero["staminaCur"] > 0:
        player.TheHero["staminaCur"] -= 1
    elif player.TheHero["staminaCur"] < 1:
        travelSpeed *= 2

    print("\n" * 13, end="")
    for x in range(5):
        if player.TheHero["healthCur"] <= 0:
            break
        print(progression, end="\r")
        if random.random() > .1:
            progression += "o "
        else:
            if enemyType["name"] != "null":
                progression += "x "
                encounter(enemyType, True)
            else:
                progression += "o "

        sleep(travelSpeed)


def climbTheGreatWiltingTree():
    clear()
    input('Climbed the great wilting tree')
    clear()


def enterTavern():
    clear()
    input("Welcome to the tavern!")
    clear()


def fallIntoAbyss():
    clear()

    input("You fall for a long time")

    player.TheHero["healthCur"] = 0

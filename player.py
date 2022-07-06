# -*- coding: utf-8 -*-
"""
Created on Fri May  8 02:25:39 2020

@author: jesse
"""

import tools
import locations
import equipment
import items
import dungeons


PlayerInventory = {
    "items": [],
    "count": [],
    "gold": 0,
}

LostItems = {
    "items": [],
    "count": [],
    "gold": 0,
    "position": {"area": None, "location": None, "subLocation": None}
}

TheHero = {
    "newPlayer": True,
    "name": "Hero Boy",
    "healthCap": 10,
    "healthCur": 10,
    "staminaCap": 8,
    "staminaCur": 8,
    "armor": 6,
    "strength": 3,
    "weapon": equipment.Fists,
    "speed": 3,
    "intelligence": 4,
    "carryCap": 10,
    "inventory": PlayerInventory,
    "statusEffect": None,
    "position": None,
    "lostItems": LostItems
}


def displayPlayerStamina():
    missingStamina = TheHero["staminaCap"] - TheHero["staminaCur"]
    remainingStamina = TheHero["staminaCap"] - missingStamina

    # name = TheHero["name"][0].upper()
    # name += TheHero["name"][1:]

    # print(missingStamina)

    filledSegment = "██" * int(remainingStamina)
    emptySegment = "░░" * int(missingStamina)
    healthBar = emptySegment + filledSegment

    print("\n" + " " * (113 - (TheHero["staminaCap"] * 2)) + " Stamina: ", end="")

    print(healthBar, end="")


def displayNameAndStatusEffect(nameOnly=False, statusOnly=False):
    name = TheHero["name"][0].upper()
    name += TheHero["name"][1:]

    if TheHero["statusEffect"]:
        statusEffect = TheHero["statusEffect"]["name"][0].upper()
        statusEffect += TheHero["statusEffect"]["name"][1:]
    else:
        nameOnly = True

    if nameOnly:
        tools.printIndent("["+name+"]", 121 - len(name), numNewLinesAfter=0)

    elif statusOnly:
        if TheHero["statusEffect"]:
            tools.printIndent("~" + statusEffect + "~", 120 - len(TheHero["statusEffect"]["name"]), numNewLinesAfter=0)

    else:
        tools.printIndent("~" + statusEffect + "~ " + "["+name+"]", 118 - len(name) - len(TheHero["statusEffect"]["name"]), numNewLinesAfter=0)

    return name


def displayPlayerInfo():
    displayNameAndStatusEffect()
    tools.displayHealth(TheHero, isPlayer=True)
    displayPlayerStamina()
    displayGold()


def displayPlayerInventory():
    inventory = True
    optionsString = "  "
    spacing = 15
    # item = 0
    # count = 1

    while inventory:
        tools.clear()

        print("\n" * 4, end="")

        displayPlayerInfo()

        print("\n" * 2, end="")

        for idx, item in enumerate(TheHero["inventory"]["items"]):
            print("  item " + str(idx + 1) + ": ", end="")
            print("(×" + str(TheHero["inventory"]["count"][idx]) + ") " + item["name"] + " " + items.getItemUsage(item))
            if idx == 3:
                optionsString += "\n    "
                spacing -= 1
            optionsString += "[" + str(idx + 1) + "] Use " + item["name"] + " | "

        optionsString += "[E]xit inventory\n\n    I want to: "

        print("\n" * (spacing - len(TheHero["inventory"]["items"])))

        selected = input(optionsString).lower()

        for idx, item in enumerate(TheHero["inventory"]["items"]):
            if selected == str(idx + 1):
                eval(item["use"])
                # useItem(TheHero["inventory"]["items"][idx])
                selected = "p"

        if selected == "e":
            inventory = False
        elif selected == "p":
            pass
        else:
            input("  Invalid selection...")

        optionsString = "  "

        spacing = 15


def displayGold():
    currentGold = str(TheHero["inventory"]["gold"])
    goldLength = len(currentGold)
    print("\n" + " " * (117 - goldLength) + "Gold: " + str(TheHero["inventory"]["gold"]), end="")


def plunderChest(size):
    offset = 44

    if size == "small":
        gold = 47
        tools.clear()
        tools.inputIndent("1 " + items.largeHealthPotion["name"] + " acquired\n", offset, 11)
        tools.inputIndent("1 " + items.smallLoafOfBread["name"] + " acquired\n", offset)
        tools.inputIndent(str(gold) + " gold " + "acquired\n", offset)
        acquireItem(items.largeHealthPotion)
        acquireItem(items.smallLoafOfBread)
        TheHero["inventory"]["gold"] += gold

    elif size == "medium":
        gold = 256
        uhpCount = 1
        fcpCount = 2
        slbCount = 4
        tools.clear()
        tools.inputIndent(str(uhpCount) + " " + items.ultraHealthPotion["name"] + "s acquired\n", offset, 11)
        tools.inputIndent(str(fcpCount) + " " + items.freshCherryPie["name"] + "s acquired\n", offset)
        tools.inputIndent(str(slbCount) + " " + items.smallLoafOfBread["name"] + " acquired\n", offset)
        tools.inputIndent(str(gold) + " gold " + "acquired\n", offset)
        acquireItem(items.ultraHealthPotion, uhpCount)
        acquireItem(items.freshCherryPie, fcpCount)
        acquireItem(items.smallLoafOfBread, slbCount)
        TheHero["inventory"]["gold"] += gold

    elif size == "large":
        gold = 999
        uhpCount = 4
        fcpCount = 5
        tools.clear()
        tools.inputIndent(str(uhpCount) + " " + items.ultraHealthPotion["name"] + "s acquired\n", offset, 11)
        tools.inputIndent(str(fcpCount) + " " + items.freshCherryPie["name"] + "s acquired\n", offset)
        tools.inputIndent("1 " + items.potionOfAscendance["name"] + " acquired\n", offset)
        tools.inputIndent(str(gold) + " gold " + "acquired\n", offset)
        acquireItem(items.ultraHealthPotion, uhpCount)
        acquireItem(items.freshCherryPie, fcpCount)
        acquireItem(items.potionOfAscendance)
        TheHero["inventory"]["gold"] += gold

    elif size == "ascendant":
        input(offset + "1 " + items.potionOfAscendance["name"] + " acquired\n")
        acquireItem(items.potionOfAscendance)


def acquireLoot(enemy):
    currentGold = TheHero["inventory"]["gold"]
    currentGold += enemy["loot"][1]
    TheHero["inventory"]["gold"] = currentGold


def acquireItem(newItem, count = 1):
    acquired = False

    for idx, item in enumerate(TheHero["inventory"]["items"]):
        if item["name"] == newItem["name"]:
            TheHero["inventory"]["count"][idx] += count
            acquired = True
            break

    if not acquired:
        TheHero["inventory"]["items"].append(newItem)
        TheHero["inventory"]["count"].append(1)


def expoundAcquiredItem(newItem, spacing):
    input(spacing + "Acquired 1 " + newItem["name"])
    acquireItem(newItem)


def purchaseItem(newItem):
    if TheHero["inventory"]["gold"] >= newItem["cost"]:
        TheHero["inventory"]["gold"] -= newItem["cost"]
        acquireItem(newItem)
        input("      Purchased 1 " + newItem["name"])
    else:
        input("  Insufficient funds...")


def displayMap(*display):

    if TheHero["position"]["location"] == "dungeons.SunkenCitadel":
        if tools.searchList(items.sunkenCitadelMap, TheHero["inventory"]["items"]):
            if display:
                dungeons.displaySunkenCitadelMap()

            return True

    elif TheHero["position"]["location"] == "dungeons.CaveOfDark":
        if tools.searchList(items.sunkenCitadelMap, TheHero["inventory"]["items"]):
            if display:
                dungeons.displayCaveOfDarkMap()

            return True

    return False

def useItem(item):
    effect = 0

    if item["effect"][effect] == "health":
        usePotion(item)

    elif item["effect"][effect] == "stamina":
        useFood(item)

    elif item["effect"][effect] == "ascend":
        ascend(item)

    elif item["effect"][effect] == "map":
        eval(item["effect"]["use"])

    tools.saveInfo()


def useFood(food):
    staminaValue = 1
    replenishedStamina = food["effect"][staminaValue]

    if TheHero["staminaCur"] != TheHero["staminaCap"]:
        if removeItem(food):
            if replenishedStamina + TheHero["staminaCur"] >= TheHero["staminaCap"]:
                TheHero["staminaCur"] = TheHero["staminaCap"]
                replenishedStamina = "to full"
            else:
                TheHero["staminaCur"] += replenishedStamina

        input("Restored " + str(replenishedStamina) + " stamina")

    else:
        input("  Stamina already full...")


def usePotion(potion):
    healthValue = 1
    replenishedHealth = potion["effect"][healthValue]

    if TheHero["healthCur"] != TheHero["healthCap"]:
        if removeItem(potion):
            if replenishedHealth + TheHero["healthCur"] >= TheHero["healthCap"]:
                TheHero["healthCur"] = TheHero["healthCap"]
                replenishedHealth = "to full"
            else:
                TheHero["healthCur"] += replenishedHealth

        input("Restored " + str(replenishedHealth) + " health")

    else:
        input("  Health already full...")


def ascend(potion):
    tools.clear()
    tools.printIndent("Consume this potion of ascendance in order to permanently increase one of your attributes", 16, 8)
    tools.printIndent("[1] Increase maximum health | [2] Increase maximum stamina | [3] Increase strength", 18, 1)
    selected = tools.inputIndent("I want to: ",4,16)

    if selected == "1":
        if removeItem(potion):
            TheHero["healthCap"] += 2
            input("Maximum health increased")

    elif selected == "2":
        if removeItem(potion):
            TheHero["staminaCap"] += 2
            input("Maximum stamina increased")

    elif selected == "3":
        if removeItem(potion):
            TheHero["strength"] += 4
            input("Maximum strength increased")


def removeItem(theItem):
    for idx, item in enumerate(TheHero["inventory"]["items"]):
        if item["name"] == theItem["name"]:
            TheHero["inventory"]["count"][idx] -= 1
            if TheHero["inventory"]["count"][idx] < 1:
                TheHero["inventory"]["items"].pop(idx)
                TheHero["inventory"]["count"].pop(idx)

            tools.saveInfo()
            return True


def storeLostItems():
    TheHero["lostItems"]["position"] = TheHero["position"]
    TheHero["lostItems"]["gold"] = TheHero["inventory"]["gold"]
    TheHero["lostItems"]["items"] = TheHero["inventory"]["items"]
    TheHero["lostItems"]["count"] = TheHero["inventory"]["count"]


def reclaimLostItems():
    if TheHero["lostItems"]["gold"] > 0 or TheHero["lostItems"]["items"] != []:
        tools.clear()
        print("\n" * 20 + " " * 40, end="")
        input("You have run into your lost items")

        tools.clear()

        TheHero["inventory"]["gold"] += TheHero["lostItems"]["gold"]

        for idx, x in enumerate(TheHero["lostItems"]["items"]):
            for y in range(TheHero["lostItems"]["count"][idx]):
                acquireItem(x)
                # input(x)

        clearLostItems()


def clearLostItems():
    TheHero["lostItems"] = {
        "items": [],
        "count": [],
        "gold": 0,
        "position": {"area": None, "location": None, "subLocation": None}
    }

    tools.saveInfo()


def deathProcess():
    tools.clear()
    storeLostItems()

    input("\n" * 13 + " " * 55 + "You died...")

    # Reset player values
    TheHero["healthCur"] = TheHero["healthCap"]
    TheHero["staminaCur"] = TheHero["staminaCap"]
    TheHero["inventory"]["gold"] = 0
    TheHero["statusEffect"] = None
    TheHero["inventory"]["items"] = []
    TheHero["inventory"]["count"] = []
    TheHero["position"] = {"area": "ThePlains", "location": "Central", "subLocation": None}

    tools.saveInfo()


def playerOptions(optionsList):

    if TheHero["position"]["subLocation"] is None:
        print("\n    [O]pen inventory | [V]iew player status | [R]eturn to Main Menu | [E]xit Game", end="")
    else:
        print("\n    [O]pen inventory | [V]iew player status", end="")

        if displayMap():
            print(" | [E]xamine map", end="")

    selected = input("\n\n    I want to: ").lower()

    for x in range(len(optionsList)):
        if tools.searchList(selected, optionsList):
            return selected

    if len(selected) == 1:
        if selected == "e":
            if TheHero["position"]["subLocation"] is None:
                tools.saveInfo()
                exit()
            elif displayMap(True):
                return False
            else:
                tools.inputIndent("Invalid selection...")

        elif selected == "o":
            displayPlayerInventory()

        elif selected == "v":
            tools.inputIndent("status", 6)

        elif selected == "r":
            if TheHero["position"]["subLocation"] is None:
                return "main"
            else:
                return "bad"
        else:
            tools.inputIndent("Invalid selection...")
            return False
    else:
        return tools.speakSecretPhrase(selected)

    tools.clear()


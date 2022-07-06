# -*- coding: utf-8 -*-
"""
Created on Tue May 12 17:25:21 2020

@author: jesse
"""
import os
import player
import locations
import base64
import dungeons
import npc
import os
import sys
import _thread
from time import sleep

clear = lambda: os.system('cls')  # on Windows System

os.system('mode con: cols=124 lines=30')

attackSpacing = 18
blockSpacing = attackSpacing - 2

swordArt = (
        " " * attackSpacing + "_|_\n" +
        " " * attackSpacing + "|||\n" +
        " " * attackSpacing + "|||\n" +
        " " * attackSpacing + "|||\n" +
        " " * attackSpacing + "\|/"
)

shieldArt = (
        " " * blockSpacing + " _____\n" +
        " " * blockSpacing + "|     |\n" +
        " " * blockSpacing + "| \\-/ |\n" +
        " " * blockSpacing + "|  |  |\n" +
        " " * blockSpacing + " \___/"
)


def displayHealth(entity, isPlayer=False):
    healthBar = ""
    offset = 2
    missingHealth = entity["healthCap"] - entity["healthCur"]
    remainingHealth = entity["healthCap"] - missingHealth

    name = entity["name"][0].upper()
    name += entity["name"][1:]

    # print(missingHealth)

    if entity["healthCap"] < 30:
        filledSegment = "██" * int(remainingHealth)
        emptySegment = "░░" * int(missingHealth)
    else:
        filledSegment = "█" * int(remainingHealth)
        emptySegment = "░" * int(missingHealth)
        offset = 1

    healthBar = emptySegment + filledSegment

    if isPlayer:
        print("\n" + " " * (114 - (entity["healthCap"] * offset)) + " Health: ", end="")
    else:
        # printIndent("-"*122,numNewLinesBefore=1)
        printIndent(name + " health: ", 114 - (entity["healthCap"] * offset) - len(name), numNewLinesBefore=2, numNewLinesAfter=0)
        # printIndent("-" * 122, numNewLinesBefore=1)

    print(healthBar, end="")

    # printIndent("-" * 122, numNewLinesBefore=1)
    # if not isPlayer:
    #     print("  Health: ", end="")


def damageEntity(entity, attacker, rating):
    initialEntityHealth = entity["healthCur"]

    weaponWeight = attacker["weapon"]["weight"]
    weaponDamage = attacker["weapon"]["damage"]
    attackerStrength = attacker["strength"]
    attackerDamage = weaponDamage + (attackerStrength - weaponWeight) / 10
    # print((attackerStrength - weaponWeight)/10)
    attackerDamage *= rating
    # print("entity:",entity["name"],"\nattacker:",attacker["name"],"\ntotal Damage:",attackerDamage)
    attackerDamage = round(attackerDamage)
    currentHealth = entity["healthCur"]

    attackerDamage -= damageNegation(entity)

    if attackerDamage > 0:
        currentHealth -= attackerDamage

    if currentHealth < 0:
        currentHealth = 0

    entity["healthCur"] = currentHealth

    # print("entity:",entity["name"],"\nattacker:",attacker["name"],"\ntotal Damage:",attackerDamage)
    saveInfo()

    if entity["healthCur"] < initialEntityHealth:
        return True
    else:
        return False


def damageNegation(entity):
    negatedDamage = 0

    if entity["armor"] >= 20:
        negatedDamage = 2

    elif entity["armor"] >= 10:
        negatedDamage = 1

    return negatedDamage


def attackInput(a_list):
    input()
    a_list.append(True)


def displayActionBar(enemy, action):
    entityDamaged = False

    a_list = []
    missBegOffset = "-" * 20
    missEndOffset = "-" * 5
    badOffset = "-" * 12
    goodOffset = " " * 6
    excellentOffset = "\|/"
    count = 0
    barOffset = " " * 30
    progressSpeed = .011
    speedDiff = (player.TheHero["speed"] - enemy["speed"]) / 5000
    barLength = len(missBegOffset) + len(missEndOffset) + (2 * len(badOffset)) + (2 * len(goodOffset)) + len(
        excellentOffset)
    progression = barOffset + "█"
    rating = ["Failed", 0]
    attackSleepTime = progressSpeed + speedDiff + player.TheHero["speed"] / 1000
    blockSleepTime = progressSpeed + (speedDiff * 10) - enemy["speed"] / 5000

    badBeg = len(missBegOffset)
    goodBeg = badBeg + len(badOffset)
    excellentBeg = goodBeg + len(goodOffset)

    excellentEnd = goodBeg + len(goodOffset) + len(excellentOffset)
    goodEnd = excellentEnd + len(goodOffset)
    badEnd = goodEnd + len(badOffset)

    barVisual = "\n" + barOffset + missBegOffset + badOffset + goodOffset + excellentOffset + goodOffset + badOffset + missEndOffset

    if attackSleepTime <= 0:
        attackSleepTime = 0.0001

    if blockSleepTime <= 0:
        blockSleepTime = 0.0001

    print(barVisual)

    for x in range(4):
        print(" " * (53 - len(action)) + action[0].upper() + action[1:] + "ing in: " + str(abs(x - 3)), end="\r")
        sleep(.17)

    _thread.start_new_thread(attackInput, (a_list,))
    while not a_list and count < barLength:
        count += 1
        print(progression, end="\r")
        progression += "█"
        if action == "attack":
            sleep(attackSleepTime)
        else:
            sleep(blockSleepTime)

    if count < badBeg or count >= badEnd:
        if action == "attack":
            rating = ["Failed", 0]
        else:
            rating = ["Failed", 1]

    if badBeg < count <= badEnd:
        if action == "attack":
            rating = ["Bad", .5]
        else:
            rating = ["Bad", .75]

    if goodBeg < count <= goodEnd:
        if action == "attack":
            rating = ["Good", 1]
        else:
            rating = ["Good", .50]

    if excellentBeg < count <= excellentEnd:
        if action == "attack":
            rating = ["Excellent", 1.5]
        else:
            rating = ["Excellent", 0]

    if action == "attack":
        entityDamaged = damageEntity(enemy, player.TheHero, rating[1])
    else:
        entityDamaged = damageEntity(player.TheHero, enemy, rating[1])

    attackBlockResults(rating[0], action, rating[1], enemy, barVisual, barOffset, count)

    return entityDamaged


def attackBlock(enemy, action):
    entityDamaged = False

    clear()

    print("\n" * 4, end="")

    if player.TheHero["statusEffect"]:
        player.displayNameAndStatusEffect()
    else:
        player.displayNameAndStatusEffect(nameOnly=True)

    displayHealth(player.TheHero, True)

    displayHealth(enemy)

    if action == "attack":
        printIndent("", numNewLinesAfter=2)
        printIndent(swordArt, 0)
    else:
        printIndent("", numNewLinesAfter=2)
        printIndent(shieldArt, 0)

    entityDamaged = displayActionBar(enemy, action)

    if action == "attack":
        action = "block"
    else:
        action = "attack"

    if enemy["healthCur"] > 0 and player.TheHero["healthCur"] > 0:
        input("\n" + " " * 50 + "Now prepare to " + action + "!")
    elif enemy["healthCur"] > 0:
        print()
    else:
        input("\n" + " " * 50 + "You have slain the " + enemy["name"] + "!")

    return entityDamaged


def attackBlockResults(ratingText, action, ratingValue, enemy, barVisual, barOffset, count):
    clear()

    print("\n" * 4, end="")

    if player.TheHero["statusEffect"]:
        player.displayNameAndStatusEffect()
    else:
        player.displayNameAndStatusEffect(nameOnly=True)

    displayHealth(player.TheHero, True)

    displayHealth(enemy)

    if action == "attack":
        printIndent("", numNewLinesAfter=2)
        printIndent(swordArt, 0)
    else:
        printIndent("", numNewLinesAfter=2)
        printIndent(shieldArt, 0)

    print(barVisual)
    print(barOffset + "█" * count)

    if player.TheHero["healthCur"] > 0:
        print("\n" + " " * 58 + ratingText + " " + action)


def characterCreation():
    isValid = False

    while not isValid:
        clear()
        printIndent("Hello traveler. What would you like to be called?", 2, 1)
        name = inputIndent("My name is: ", 4, 0, 0)

        if name.isalpha():
            isValid = True
        else:
            inputIndent("Invalid entry")

    player.TheHero["name"] = name

    player.TheHero["newPlayer"] = False

    player.TheHero["position"] = {"area": "ThePlains", "location": "Central", "subLocation": None}

    saveInfo()


def beginStory():
    clear()
    speaking = "Generic Intro Boy: "

    inputIndent(speaking+"Well well well. Look who finally decided to show back up." )
    inputIndent(speaking+"A miracle you were able to find your way back. You really don't remember a thing, do you?")

def displaySettingsMenu():
    clear()

    print("\n\n\n  [1] Toggle quick input ")
    print("    When toggled on input will be entered automatically as opposed to needing to press the enter key")

    print("\n" * 19)
    print("  [E]xit settings")

    selected = input("\n    I want to: ").lower()

    if selected == "e":
        return "back"
    elif selected == "1":
        input("  Sorry, feature is currently not implemented. Please send complaints to 'beangoob@gmail.waz'")


def displayMainMenu():
    deciding = True

    loadInfo()

    while deciding == True:
        clear()

        print("\n\n    Welcome to\n\n")
        print("         ____                                    ______")
        print("        |----|  _        __      ___      _   __ --++--  __     ___")
        print("        ||  || | \ \  / |_  |\ |  |  | | |_) |_    ||   |_  \_/  |")
        print("        ||\\\\|| |_/  \/  |__ | \|  |  \_/ | \ |__   ||   |__ / \  |")

        print("\n" * 16, end="  ")

        if player.TheHero["newPlayer"]:
            print("[Enter] to begin your adventure", end=" | ")
        else:
            print("[Enter] to resume your adventure", end=" | ")

        print("[O]pen settings menu", end=" | ")

        if not player.TheHero["newPlayer"]:
            print("[D]elete current character", end=" | ")

        print("[E]xit game")

        selected = input("\n    I want to: ").lower()

        if selected == "d" and not player.TheHero["newPlayer"]:
            clear()
            print("\n" * 23)
            print("  Are you sure you want to delete " + player.TheHero["name"] + "?")
            print("    [Y]es delete my character | [N]o keep my character")
            if input("\n    I want to: ").lower() == "y":
                os.remove("playerInfo.sav")
                input("  Character deleted. Restarting now")
                os.execv(sys.executable, ['main'] + sys.argv)

        elif selected == "o":
            displaySettingsMenu()
        elif selected == "e":
            exit()
        elif selected == "":
            deciding = False

            if player.TheHero["newPlayer"] == True:
                characterCreation()
                # beginStory()

            clear()
        else:
            input("  Invalid selection...")

    return True


def speakSecretPhrase(phrase):
    # player.TheHero["position"] = {"area": "ThePlains", "location": "Central", "subLocation": None}
    if phrase == "revelus maximus sunken citadel":
        if player.TheHero["position"]["location"] == "dungeons.SunkenCitadel":
            if player.TheHero["position"]["subLocation"] == "C18" or player.TheHero["position"]["subLocation"] == "C2":
                if not dungeons.SunkenCitadel["passageRevealed"]:
                    dungeons.SunkenCitadel["passageRevealed"] = True
                    inputIndent("passage is revealed")
                    dungeons.SunkenCitadel["rooms"][2] = {"name": "C2", "right": "C28", "downward": "C1", "left": "C3"}
                    dungeons.SunkenCitadel["rooms"][18] = {"name": "C18", "upward": "C17", "downward": "C19", "left": "C28"}
                    saveInfo()
                    return "modify"

    elif phrase == "pls pls give me beeg boy powers":
        inputIndent("yah ok")
        player.TheHero["strength"] = 80
        player.TheHero["speed"] = 6
        player.TheHero["healthCap"] = 100
        player.TheHero["healthCur"] = 100
        player.TheHero["staminaCap"] = 25
        player.TheHero["staminaCur"] = 25
        return True

    inputIndent("Invalid selection...")

    return False


def loadInfo():
    try:
        f = open("playerInfo.sav", "r")
    except:
        f = open("playerInfo.sav", "w")

        gameInfo = str([player.TheHero, dungeons.CaveOfDark, dungeons.SunkenCitadel, npc.TheShadowMan, npc.Shaymus])
        playerInfoBytes = gameInfo.encode('ascii')
        base64Bytes = base64.b64encode(playerInfoBytes)
        base64playerInfo = base64Bytes.decode('ascii')

        f.write(base64playerInfo)

        f.close()

    else:
        gameInfo = f.read()
        playerInfoBytes = gameInfo.encode('ascii')
        base64Bytes = base64.b64decode(playerInfoBytes)
        base64playerInfo = base64Bytes.decode('ascii')

        finalInfo = eval(base64playerInfo)

        playerInfo = finalInfo[0]
        caveOfDarkInfo = finalInfo[1]
        sunkenCitadelInfo = finalInfo[2]
        shadowManInfo = finalInfo[3]
        shaymusInfo = finalInfo[4]

        player.TheHero = playerInfo
        dungeons.CaveOfDark = caveOfDarkInfo
        dungeons.SunkenCitadel = sunkenCitadelInfo
        npc.TheShadowMan = shadowManInfo
        npc.Shaymus = shaymusInfo

        f.close()


def saveInfo():
    f = open("playerInfo.sav", "w")

    gameInfo = str([player.TheHero, dungeons.CaveOfDark, dungeons.SunkenCitadel, npc.TheShadowMan, npc.Shaymus])

    playerInfoBytes = gameInfo.encode('ascii')
    base64Bytes = base64.b64encode(playerInfoBytes)
    base64playerInfo = base64Bytes.decode('ascii')

    f.write(base64playerInfo)

    f.close()


def searchList(valueToFind, listToSearch):
    for x in listToSearch:
        if valueToFind == x:
            return True

    return False


def printIndent(dialogue, numSpaces = 2, numNewLinesBefore = 0, numNewLinesAfter = 1):
    print("\n" * numNewLinesBefore + " " * numSpaces + dialogue + "\n" * numNewLinesAfter, end="")


def inputIndent(dialogue, numSpaces = 2, numNewLinesBefore = 0, numNewLinesAfter = 0):
    finalInput = "\n" * numNewLinesBefore + " " * numSpaces + dialogue + "\n" * numNewLinesAfter

    return input(finalInput)


def processTagFunction(dungeonCopy, roomIDnum, curRoomID):

    if dungeonCopy["rooms"][roomIDnum].get("tags") is not None:
        if dungeonCopy["rooms"][roomIDnum]["tags"].get("dropdown") is not None and searchList(curRoomID, dungeonCopy["rooms"][roomIDnum]["tags"]["dropdown"]):
            clear()
            inputIndent("You slide down a steep slope...", 40, 12)

        elif dungeonCopy["rooms"][roomIDnum]["tags"].get("climb") is not None and searchList(curRoomID, dungeonCopy["rooms"][roomIDnum]["tags"]["climb"]):
            clear()
            inputIndent("You climb the ladder and push open the one-way trap door...", 30, 12)


def roomOutput(dungeonCopy, roomIDnum, optionsList, keys, directionalOptions):
    for x in range(4):
        if optionsList[x] is not None:
            print("[" + keys[x] + "] Venture " + directionalOptions[x], end="")

            if dungeonCopy["rooms"][roomIDnum].get("tags") is not None:
                if dungeonCopy["rooms"][roomIDnum]["tags"].get("dropdown") is not None and searchList(optionsList[x], dungeonCopy["rooms"][roomIDnum]["tags"]["dropdown"]):
                    print(" (drop down)", end="")

                elif dungeonCopy["rooms"][roomIDnum]["tags"].get("climb") is not None and searchList(optionsList[x], dungeonCopy["rooms"][roomIDnum]["tags"]["climb"]):
                    print(" (climb ladder)", end="")

            if x < 3 and optionsList[x + 1] is not None:
                    print(" | ", end="")

        elif dungeonCopy["rooms"][roomIDnum].get("tags") is not None and dungeonCopy["rooms"][roomIDnum]["tags"].get("trapdoor"):
            if searchList(directionalOptions[x], dungeonCopy["rooms"][roomIDnum]["tags"].get("trapdoor")):
                if optionsList[x - 1] is not None:
                    print(" | ", end="")
                print("[I]nspect trap door", end="")
            else:
                print(" ... " * 4, end="")
            if len(dungeonCopy["rooms"][roomIDnum]["tags"]["trapdoor"]) > 1:
                print(" | ", end="")
            elif x < 3 and optionsList[x + 1] is not None:
                print(" | ", end="")

        elif dungeonCopy["rooms"][roomIDnum].get("tags") is not None and dungeonCopy["rooms"][roomIDnum]["tags"].get("enchanted wall"):
            if searchList(directionalOptions[x], dungeonCopy["rooms"][roomIDnum]["tags"].get("enchanted wall")):
                if optionsList[x - 1] is not None:
                    print(" | ", end="")
                print("[I]nspect ornate wall", end="")
            else:
                print(" ... " * 4, end="")
            if len(dungeonCopy["rooms"][roomIDnum]["tags"]["enchanted wall"]) > 1:
                print(" | ", end="")
            elif x < 3 and optionsList[x + 1] is not None:
                print(" | ", end="")
        else:
            print(" ... " * 4, end="")


def gameTick(action = "attack"):
    if player.TheHero["statusEffect"] and action == "attack":
        if player.TheHero["statusEffect"]["name"] == "envenomated" and player.TheHero["statusEffect"]["duration"] > 0:
            player.TheHero["statusEffect"]["duration"] -= 1
            if player.TheHero["healthCur"] > 1:
                player.TheHero["healthCur"] -= 1

        if player.TheHero["statusEffect"]["duration"] == 0:
            player.TheHero["statusEffect"] = None

    saveInfo()

# -*- coding: utf-8 -*-
"""
Created on Tue May 12 18:10:30 2020

@author: jesse
"""

import player
import tools
import equipment
import dungeons

Null = {
    "name": "null",
    "healthCap": 0,
    "healthCur": 0,
    "strength": 0,
    "weapon": {"name": "null", "damage": 0, "weight": 0},
    "speed": 0,
    "intelligence": 0,
    "loot": ["gold", 0]
}

Brownie = {
    "name": "brownie",
    "healthCap": 3,
    "healthCur": 3,
    "strength": 2,
    "weapon": equipment.Claws,
    "armor": 1,
    "speed": 1,
    "intelligence": 1,
    "loot": ["gold", 9]
}

FeralVole = {
    "name": "feral vole",
    "healthCap": 3,
    "healthCur": 3,
    "strength": 4,
    "weapon": equipment.Claws,
    "armor": 1,
    "speed": 3,
    "intelligence": 1,
    "loot": ["gold", 2]
}

Goblin = {
    "name": "goblin",
    "healthCap": 5,
    "healthCur": 5,
    "strength": 8,
    "weapon": equipment.Dagger,
    "armor": 4,
    "speed": 3,
    "intelligence": 2,
    "loot": ["gold", 18]
}

Golem = {
    "name": "obsidian golem",
    "healthCap": 8,
    "healthCur": 8,
    "strength": 1000,
    "weapon": equipment.Fists,
    "armor": 22,
    "speed": 0,
    "intelligence": 1,
    "loot": ["gold", 117]
}


JuvenileBasilisk = {
    "name": "juvenile basilisk",
    "healthCap": 4,
    "healthCur": 4,
    "strength": 4,
    "weapon": equipment.Fangs,
    "armor": 2,
    "speed": 8,
    "intelligence": 1,
    "loot": ["gold", 59],
    "ability": "venom bite",
}


def venomBite(playerDamaged, action):
    maxDuration = 6

    if action == "attack":
        if playerDamaged:
            if player.TheHero["statusEffect"]:
                if player.TheHero["statusEffect"]["name"] == "envenomated":
                    player.TheHero["statusEffect"]["duration"] += 2
                    if player.TheHero["statusEffect"]["duration"] > maxDuration:
                        player.TheHero["statusEffect"]["duration"] = 6
            else:
                player.TheHero["statusEffect"] = {"name": "envenomated", "duration": 3}
                tools.inputIndent("*You have been envenomated*")


UndeadWarrior = {
    "name": "undead warrior",
    "healthCap": 15,
    "healthCur": 8,
    "strength": 0,
    "weapon": equipment.LongSword,
    "armor": 8,
    "speed": 1,
    "intelligence": 1,
    "loot": ["gold", 12]
}


GoblinChieftain = {
    "name": "goblin chieftain",
    "healthCap": 20,
    "healthCur": 20,
    "strength": 30,
    "weapon": equipment.Fists,
    "armor": 8,
    "speed": 3,
    "intelligence": 2,
    "loot": ["gold", 144],
    "ability": "enrage",
    "enraged": False
}

def enrage(newGoblinChieftain):
    tools.clear()
    if newGoblinChieftain["healthCur"] <= 6 and not newGoblinChieftain["enraged"]:
        tools.inputIndent("The goblin chieftain enrages", 20, 8)
        newGoblinChieftain["strength"] = 1000
        newGoblinChieftain["enraged"] = True

    return True

SpectralSandworm = {
    "name": "spectral sandworm",
    "healthCap": 50,
    "healthCur": 50,
    "strength": 50,
    "weapon": equipment.SerratedTeeth,
    "armor": 0,
    "speed": 9,
    "intelligence": 1,
    "loot": ["gold", 3430],
    "ability": "burrowAndFlee",
    "healthRegen": 0,
    "stages": {"stage1": False, "stage2": False, "stage3": False},
    "location": "TE"
}


def getSpectralSandwormLocation():
    if player.TheHero["position"]["subLocation"] == SpectralSandworm["location"]:
        if not dungeons.SunkenCitadel["bossDefeated"]:
            if SpectralSandworm["healthCur"] + round(SpectralSandworm["healthRegen"]/2) >= SpectralSandworm["healthCap"]:
                SpectralSandworm["healthCur"] = SpectralSandworm["healthCap"]
                SpectralSandworm["healthRegen"] = 0
            else:
                SpectralSandworm["healthCur"] += round(SpectralSandworm["healthRegen"]/2)
                SpectralSandworm["healthRegen"] = 0
            encounter(SpectralSandworm)

    if SpectralSandworm["stages"]["stage1"] and not SpectralSandworm["stages"]["stage2"] and not SpectralSandworm["stages"]["stage3"]:
        # input("stage 1, some regen")
        SpectralSandworm["healthRegen"] += 1
    elif SpectralSandworm["stages"]["stage2"] and not SpectralSandworm["stages"]["stage3"]:
        # input("stage 2, more regen")
        SpectralSandworm["healthRegen"] += 2
    elif SpectralSandworm["stages"]["stage3"]:
        # input("stage 3, much regen")
        SpectralSandworm["healthRegen"] += 3

    if player.TheHero["healthCur"] < 1:
        return False


def burrowAndFlee(newSpectralSandworm):

    if newSpectralSandworm["healthCur"] <= 0:
        SpectralSandworm["healthCur"] = newSpectralSandworm["healthCur"]
        dungeons.SunkenCitadel["bossDefeated"] = True
        tools.clear()
        tools.inputIndent("You have conquered the Sunken Citadel!", 30, 10)
        tools.saveInfo()
        return True

    elif newSpectralSandworm["healthCur"] <= 5 and not newSpectralSandworm["stages"]["stage3"]:
        SpectralSandworm["healthCur"] = newSpectralSandworm["healthCur"]
        SpectralSandworm["stages"]["stage3"] = True
        SpectralSandworm["speed"] = 0
        SpectralSandworm["location"] = "D5"
        tools.clear()
        tools.inputIndent("The spectral sandworm flees to another location", 20, 8)

    elif newSpectralSandworm["healthCur"] <= 25 and not newSpectralSandworm["stages"]["stage2"]:
        SpectralSandworm["healthCur"] = newSpectralSandworm["healthCur"]
        SpectralSandworm["stages"]["stage2"] = True
        SpectralSandworm["speed"] = 5
        SpectralSandworm["location"] = "D2"
        tools.clear()
        tools.inputIndent("The spectral sandworm flees to another location", 20, 8)

    elif newSpectralSandworm["healthCur"] <= 35 and not newSpectralSandworm["stages"]["stage1"]:
        SpectralSandworm["healthCur"] = newSpectralSandworm["healthCur"]
        SpectralSandworm["stages"]["stage1"] = True
        SpectralSandworm["speed"] = 8
        SpectralSandworm["location"] = "D1"
        tools.clear()
        tools.inputIndent("The spectral sandworm flees to another location", 20, 8)

    else:
        return True

    return False


def restoreSandwormState():
    if not dungeons.SunkenCitadel["bossDefeated"]:
        SpectralSandworm["healthCur"] = 50
        SpectralSandworm["stages"] = {"stage1": False, "stage2": False, "stage3": False}
        SpectralSandworm["healthRegen"] = 0
        SpectralSandworm["healthRegen"] = 9
        SpectralSandworm["location"] = "TE"


def determineAbility(enemy, playerDamaged, enemyDamaged, action):
    if enemy["name"] == "spectral sandworm":
        return burrowAndFlee(enemy)

    elif enemy["name"] == "goblin chieftain":
        return enrage(enemy)

    elif enemy["name"] == "juvenile basilisk":
        venomBite(playerDamaged, action)

    return True



def encounter(enemy, *travelEncounter):
    tools.clear()
    newEnemy = enemy.copy()
    fighting = True

    if player.TheHero["speed"] > enemy["speed"]:
        action = "attack"
    else:
        action = "block"

    if action == "attack":
        tools.printIndent("", numNewLinesBefore=9)
        tools.printIndent(tools.swordArt, 0)
    else:
        tools.printIndent("", numNewLinesBefore=9)
        tools.printIndent(tools.shieldArt, 0)

    print("\n" * 2, end="")
    print(" " * 34 + "You've encountered a " + newEnemy["name"] + ". ", end="")

    if travelEncounter != (): # NEED TO MAKE FLEE CHANCE BASED ON SPEED STAT DIFF, LOOK IN NOTES FOR DETAILS
        print("\n"*8 + " "*2 + "[A]ttempt to flee | [Enter] to stand fight")
        selected = input("\n    I will: ")
        if selected.lower() == "a":
            if player.TheHero["staminaCur"] >= 1:
                player.TheHero["staminaCur"] -= 1
                input(" "*2 + "Fled successfully")
                tools.clear()
                print("\n" * 13, end="")
                return
            else:
                input(" " * 2 + "Cannot flee without sufficient stamina..." + " Prepare to " + action + "!")
                # input(" " * 34 + "Prepare to " + action + "!\n")
    else:
        input("Prepare to " + action + "!\n")

    while newEnemy["healthCur"] > 0 and player.TheHero["healthCur"] > 0:
        enemyDamaged = False
        playerDamaged = False

        tools.gameTick(action)

        if action == "attack":
            enemyDamaged = tools.attackBlock(newEnemy, action)
            action = "block"
        else:
            playerDamaged = tools.attackBlock(newEnemy, action)
            action = "attack"

        if player.TheHero["healthCur"] < 1:
            return False

        if newEnemy.get("ability"):
            fighting = determineAbility(newEnemy, playerDamaged, enemyDamaged, action)
            if not fighting:
                return

    player.acquireLoot(newEnemy)
    tools.clear()
    print("\n" * 13, end="")

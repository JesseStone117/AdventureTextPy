# -*- coding: utf-8 -*-
"""
Created on Fri May  8 02:07:58 2020

@author: jesse
"""

from time import sleep
from tools import clear
from tools import saveInfo
from enemy import encounter
import random
import items
import player
import dungeons
import npc
import enemy

Town = {
    "name": "Town",
    "option1": "Go right to the plains",
    "option2": "Enter tavern",
    "option3": "Approach Shopkeep",
    "option4": "",
    "enemies": [enemy.Null]
}

ThePlains = {
    "name": "The Plains",
    "option1": "Go left to town",
    "option2": "Go right to wilderness",
    "option3": "Talk to the shadow man",
    "option4": "Provoke the shadow man",
    "enemies": [enemy.Null]
}

TheWilderness = {
    "name": "The Wilderness",
    "option1": "Go left to the plains",
    "option2": "Go right to the marsh",
    "option3": "",
    "option4": "",
    "enemies": [enemy.Brownie]
}

TheMarsh = {
    "name": "The Marsh",
    "option1": "Go left to wilderness",
    "option2": "Go right to Blighteth",
    "option3": "Enter the cave of dark",
    "option4": "Climb the great wilting tree",
    "enemies": [enemy.Brownie]
}

Blighteth = {
    "name": "Blighteth",
    "option1": "Go left to the marsh",
    "option2": "Go right to the deep",
    "option3": "",
    "option4": "",
    "enemies": [enemy.Goblin]
}

TheDeep = {
    "name": "The Deep",
    "option1": "",
    "option2": "",
    "option3": "",
    "option4": "",
    "enemies": [enemy.Null]
}

Areas = [Town, ThePlains, TheWilderness, TheMarsh, Blighteth, TheDeep]

def locationOptions(selected, currentArea):
    if currentArea["name"] == "Town":
        return townOptions(selected)
    
    if currentArea["name"] == "The Plains":
        return plainsOptions(selected)
    
    if currentArea["name"] == "The Wilderness":
        return wildernessOptions(selected)
    
    if currentArea["name"] == "The Marsh":
        return marshOptions(selected)
    
    if currentArea["name"] == "Blighteth":
        return blightethOptions(selected)
    
    if currentArea["name"] == "The Deep":
        return deepOptions(selected)
    
    
def townOptions(selected):
    if selected == 1:
        return ThePlains
    
    if selected == 2:
        clear()
        input ("\n" *3 + "  Welcome to the tavern")
        
        return Town
    
    if selected == 3:
        npc.talkToTheShopkeep()
        return Town
    
def plainsOptions(selected):
    if selected == 1:
        return Town
    
    if selected == 2:
        return TheWilderness
    
    if selected == 3:
        npc.talkToTheShadowMan()
        return ThePlains
    
    if selected == 4:
        clear()
        input("\n" *3 + "  The Shadow Man: You'll wish you hadn't done that...")
        player.TheHero["healthCur"] = 0
        return ThePlains

def wildernessOptions(selected):
    if selected == 1:
        return ThePlains
    
    if selected == 2:
        return TheMarsh
    
    if selected == 3:
        return TheWilderness
    
    if selected == 4:
        return TheWilderness

def marshOptions(selected):
    if selected == 1:
        return TheWilderness
    
    if selected == 2:
        return Blighteth
    
    if selected == 3:
        dungeons.enterCaveOfDark()
        return TheMarsh
    
    if selected == 4:
        clear()
        selection = input("\n" *3 + "  Atop the great wilting tree... ").lower()
        if selection == "shaymus":
            npc.talkToShaymus()
        return TheMarsh
    
def blightethOptions(selected):
    if selected == 1:
        return TheMarsh
    
    if selected == 2:
        return TheDeep
    
    if selected == 3:
        return Blighteth
    
    if selected == 4:
        return Blighteth
    
def deepOptions(selected):
    if selected == 1:
        return TheDeep
    
    if selected == 2:
        return TheDeep
    
    if selected == 3:
        return TheDeep
    
    if selected == 4:
        return TheDeep

def displayAreaOptions(currentArea):
    clear()
    selected = 0
    spacing = 16
    numOptions = 0
    initialLocation = currentArea["name"]
    
    print("\n\n\n {" + currentArea["name"] + "}", end="")
    
    player.displayPlayerInfo()
    
    if player.TheGameInfo.greeting == True:
        print("\n  What would you like to do, traveler?", end="")
        player.TheGameInfo.greeting = False
        # spacing = 17
    else:
        print("\n", end="")
        print("",end="")
    
    print("\n" * spacing)
    
    if currentArea["option1"] != "":
        print("  [1] " + currentArea["option1"], end="")
        numOptions += 1
    
    if currentArea["option2"] != "":
        print(" | [2] " + currentArea["option2"], end="")
        numOptions += 1
    
    if currentArea["option3"] != "":
        print(" | [3] " + currentArea["option3"], end="")
        numOptions += 1
        
    if currentArea["option4"] != "":
        print(" | [4] " + currentArea["option4"], end="")
        numOptions += 1
        
    # print ("\n    [O]pen inventory | [P]layer Status | [E]xit Game", end="")
    
    # selected = input("\n\n    I want to: ").lower()
    selected = player.playerOptions()
    
    if selected != True:
        try:
            selected = int(selected)
        except:
            selected = 0
        
        if selected > numOptions or selected < 1:
            input("  Invalid selection...")
            selected = 0
        
        if selected > 0 and selected <= numOptions:
            currentArea = locationOptions(selected, currentArea)
            areaEnemyType = currentArea["enemies"][0]
            player.TheHero["location"] = currentArea["name"]
            
        if initialLocation != currentArea["name"]:
            travel(areaEnemyType)
            
    saveInfo()
    return currentArea
    clear()
    
def travel(enemy):
    clear()
    progression = " "*46 + "Traveling: " + "o "
    travelSpeed = 0.15
    if player.TheHero["staminaCur"] > 0:
        player.TheHero["staminaCur"] -= 1
    elif player.TheHero["staminaCur"] < 1:
        travelSpeed *= 2
    
    print("\n"*13, end="")
    for x in range(5):
        if player.TheHero["healthCur"] <= 0:
            break;
        print(progression, end="\r")
        if random.random() > .1:
            progression += "o "
        else:
            if enemy["name"] != "null":
                progression += "x "
                encounter(enemy)
            else:
                progression += "o "
                
        sleep(travelSpeed)
        
    

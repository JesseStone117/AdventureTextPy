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

def enterRoom(dungeon, curRoomID):
    dungeonName = dungeon["name"]
    roomIDnum = 0
    leftRoom = ""
    rightRoom = ""
    forwardRoom = ""
    backwardRoom = ""
    enemyCount = 1
    enemyType = ""
    loot = ""
    
    optionsList = []
    numOptions = 0
    optionsString = ""
    
    tools.clear()
    
    rooms = list(dungeon["rooms"])
    
    count = 0
    
    for idx in rooms:
        # print(idx)
        if idx["name"] == curRoomID:
            roomIDnum = count
        count += 1
    
    # print("Room ID:", rooms[roomIDnum]["name"])
    # print("Room ID number:", roomIDnum)
    
    for x in rooms[roomIDnum].items():
        # if x[0] == "name":
            # roomID = x[1]
            
        if x[0] == "left":
            leftRoom = x[1]
        
        elif x[0] == "right":
            rightRoom = x[1]
            
        elif x[0] == "forward":
            forwardRoom = x[1]
            
        elif x[0] == "backward":
            backwardRoom = x[1]
            
        elif x[0] == "enemy":
            enemyType = x[1]
            
        elif x[0] == "enemyCount":
            enemyCount = x[1]
            
        elif x[0] == "loot":
            loot = x[1]
            
    
    if enemyType != "":
        for x in range(enemyCount):
            if enemy.encounter(enemyType) == False:
                return "L"
    
    dungeon["rooms"][roomIDnum]["enemy"] = ""
    
    tools.clear()
    
    optionsString += "  "
    
    if leftRoom != "":
        numOptions += 1
        optionsList.extend([leftRoom])
        optionsString += "[" + str(numOptions) + "] Venture left"
        
    if forwardRoom != "":
        if numOptions > 0:
            optionsString += " | "
        numOptions += 1
        optionsList.extend([forwardRoom])
        
        optionsString += "[" + str(numOptions) + "] Venture forward"
    
    if backwardRoom != "":
        if numOptions > 0:
            optionsString += " | "
        numOptions += 1
        optionsList.extend([backwardRoom])
        
        optionsString += "[" + str(numOptions) + "] Venture backward"
        
    if rightRoom != "":
        if numOptions > 0:
            optionsString += " | "
        numOptions += 1
        optionsList.extend([rightRoom])
        
        optionsString += "[" + str(numOptions) + "] Venture right"
        
    if curRoomID == "E":
        optionsString += " | [L]eave " + dungeonName.lower()
    
    if curRoomID == "TE" and enemyType != "":
        endOfCaveOfDark()
    
    while True:
        if curRoomID != "TE":
            print("\n\n\n {"+dungeonName+"}",end="")
        else:
            print("\n\n\n {"+dungeonName+" - Final Room}",end="")
        
        player.displayPlayerInfo()
        
        print("\n"*17)
        
        print(optionsString,end="")
        
        if loot != "":
            print(" | [S]earch chest",end="")
        
        selected = player.playerOptions()
        
        # selected = input("\n  I want to: ")
        
        if selected != True:
        
            try:
                selected = int(selected)
                # print("numoptoins",numOptions)
                if selected > numOptions or selected < 1:
                    input("  Invalid selection...")
                    selected = 0
                    
            except:
                if selected == "l" and curRoomID == "E":
                    return "L"
                
                if selected == "s" and loot != "":
                    player.searchChest(loot)
                    dungeon["rooms"][roomIDnum]["loot"] = ""
                    loot = ""
                
                else:
                    input("  Invalid input...")
                tools.clear()
            else:
                if selected == 1:
                    return optionsList[0]
                
                elif selected == 2:
                    return optionsList[1]
                    
                elif selected == 3:
                    return optionsList[2]
                
                elif selected == 4:
                    return optionsList[3]
                tools.clear()

CaveOfDark = {
    "name": "Cave of dark",
    "rooms": [
        {"name": "E", "left": "D1", "forward": "C1"},
        {"name": "D1", "right": "E", "enemy": enemy.FeralVole},
        {"name": "C1", "left": "D2", "right": "C2", "backward": "E"},
        {"name": "D2", "right": "C1", "enemy": enemy.Goblin},
        {"name": "C2", "left": "C1", "forward": "C3", "enemy": enemy.FeralVole},
        {"name": "C3", "left": "C4", "right": "D3", "forward": "D4", "backward": "C2"},
        {"name": "C4", "right": "C3", "forward": "TE", "enemy": enemy.Goblin,"enemyCount": 2},
        {"name": "TE", "backward": "C4", "enemy": enemy.GoblinChieftain},
        {"name": "D3", "left": "C3", "loot": "small"},
        {"name": "D4", "backward": "C3", "enemy": enemy.Goblin},
    ]
}

def enterCaveOfDark():
    location = "E" # Entrance
    dungeon = copy.deepcopy(CaveOfDark)
    
    tools.clear()
    
    while location != "L":
        location = enterRoom(dungeon, location)
    
def endOfCaveOfDark():
    input("you win!")
    player.TheHero["gold"] += 1000
    player.acquireItem(items.freshCherryPie)
    player.acquireItem(items.ultraHealthPotion)
    tools.clear()




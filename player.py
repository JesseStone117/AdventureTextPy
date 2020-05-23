# -*- coding: utf-8 -*-
"""
Created on Fri May  8 02:25:39 2020

@author: jesse
"""

import tools
import locations
import equipment

class GameInfo:
    def __init__(self, greeting):
        self.greeting = greeting

class Character:
    def selection(self, selected):
        True
        
    def option1(self, selected):
        if selected == 1:
            print("OK")

class Player:
    def __init__(self, name, health):
        self.name = name
        self.health = health
        
PlayerInventory = {
    "item1": {"name": "null", "weight": "null", "effect": "null", "count": "null"},
    "item2": {"name": "null", "weight": "null", "effect": "null", "count": "null"},
    "item3": {"name": "null", "weight": "null", "effect": "null", "count": "null"},
    "item4": {"name": "null", "weight": "null", "effect": "null", "count": "null"}
}

TheHero = {
    "newPlayer": True,
    "name": "Hero Boy",
    "healthCap": 10,
    "healthCur": 10,
    "staminaCap": 8,
    "staminaCur": 8,
    "armor": 1,
    "strength": 3,
    "weapon": equipment.Fists,
    "speed": 3,
    "intelligence": 4,
    "inventoryCap": 4,
    "carryCap": 10,
    "inventory": PlayerInventory,
    "gold": 0,
    "location": "The Plains"
}

def displayPlayerStamina():
    healthBar = ""
    missingStamina = TheHero["staminaCap"] - TheHero["staminaCur"]
    remainingStamina = TheHero["staminaCap"] - missingStamina
    
    name = TheHero["name"][0].upper()
    name += TheHero["name"][1:]
    
    # print(missingStamina)
    
    filledSegment = "██"*int(remainingStamina)
    emptySegment = "░░"*int(missingStamina)
    healthBar = emptySegment + filledSegment
    
    print("\n" + " "*(127-len(name)-(TheHero["healthCap"]*3)) + name + " Stamina: ", end="")
    
    print(healthBar,end="")

def displayPlayerInfo():
    tools.displayHealth(TheHero)
    displayPlayerStamina()
    displayGold()
    
def displayPlayerInventory():
    inventory = True
    optionsString = "  "
    count = 1
    
    while inventory:
        tools.clear()
        
        print("\n"*3,end="")
        
        displayPlayerInfo()
        print()
        
        for key, value in TheHero["inventory"].items():
            print("  " + key + ": ",end="")
            if value["name"] != "null":
                print(value["name"] + " " + str(value["count"]) + "\n")
                optionsString += "[" + str(count) + "] Use " + value["name"] + " | "
            else:
                print("\n")
            count += 1
            
        optionsString += "[E]xit inventory\n    I want to: "
        
        print()
        
        selected = input(optionsString).lower()
        
        if selected == "1" and TheHero["inventory"]["item1"]["name"] != "null":
            useItem(TheHero["inventory"]["item1"])
            
        elif selected == "2" and TheHero["inventory"]["item2"]["name"] != "null":
            useItem(TheHero["inventory"]["item2"])
            
        elif selected == "3" and TheHero["inventory"]["item3"]["name"] != "null":
            useItem(TheHero["inventory"]["item3"])
        
        elif selected == "4" and TheHero["inventory"]["item4"]["name"] != "null":
            useItem(TheHero["inventory"]["item4"])
            
        elif selected == "e":
            inventory = False
        else:
            input("  Invalid selection...")
        
        optionsString = "  "
        count = 1

def displayGold():
    currentGold = str(TheHero["gold"])
    goldLength = len(currentGold)
    print("\n"+" "*(117-goldLength)+"Gold: "+str(TheHero["gold"]),end="")

def acquireLoot(enemy):
    currentGold = TheHero["gold"] 
    currentGold += enemy["loot"][1]
    TheHero["gold"] = currentGold

def acquireItem(newItem):
    acquired = False
    for key, value in TheHero["inventory"].items():
        if value["name"] == newItem["name"]:
            value["count"] += 1
            acquired = True
            tools.saveInfo()
            break
            
    if acquired == False:
        for key, value in TheHero["inventory"].items():
            if value["name"] == "null":
                value["name"] = newItem["name"]
                value["weight"] = newItem["weight"]
                value["effect"] = newItem["effect"]
                value["count"] = 1
                tools.saveInfo()
                break

def purchaseItem(newItem):
    if TheHero["gold"] >= newItem["cost"]:
        TheHero["gold"] -= newItem["cost"]
        acquireItem(newItem)
        input("      Purchased 1 " + newItem["name"])
    else:
        input("  Insufficient funds...")

def useItem(item):
    if "restoreHealth" in item["effect"]:
        usePotion(item)
        
    if "restoreStamina" in item["effect"]:
        useFood(item)

def useFood(food):
    replenishedStamina = food["effect"]["restoreStamina"]
    
    if TheHero["staminaCur"] != TheHero["staminaCap"]:
        if replenishedStamina + TheHero["staminaCur"] >= TheHero["staminaCap"]:
            TheHero["staminaCur"] = TheHero["staminaCap"]
            replenishedStamina = "to full"
        else:
            TheHero["staminaCur"] += replenishedStamina
            
        for key, value in TheHero["inventory"].items():
                if value["name"] == food["name"] and value["name"] != "null":
                    value["count"] -= 1
                    input("Restored " + str(replenishedStamina) + " stamina")
                    # TheHero["healthCur"] += 
                    if value["count"] < 1:
                        value["name"] = "null"
                    tools.saveInfo()
                    break
    else:
        input("  Stamina already full...")

def usePotion(potion):
    replenishedHealth = potion["effect"]["restoreHealth"]
    
    if TheHero["healthCur"] != TheHero["healthCap"]:
        if replenishedHealth + TheHero["healthCur"] >= TheHero["healthCap"]:
            TheHero["healthCur"] = TheHero["healthCap"]
            replenishedHealth = "to full"
        else:
            TheHero["healthCur"] += replenishedHealth
        
        for key, value in TheHero["inventory"].items():
            if value["name"] == potion["name"] and value["name"] != "null":
                value["count"] -= 1
                input("Restored " + str(replenishedHealth) + " health")
                # TheHero["healthCur"] += 
                if value["count"] < 1:
                    value["name"] = "null"
                tools.saveInfo()
                break
    else:
        input("  Health already full...")

def damagePlayer(enemy):
    enemyDamage = enemy["weapon"]["damage"]+enemy["strength"]
    currentHealth = TheHero["healthCur"] 
    currentHealth -= (enemyDamage-TheHero["armor"])
    TheHero["healthCur"] = currentHealth
    tools.saveInfo()

def deathProcess():
    tools.clear()
    input("\n"*13 + " "*55 + "You died...")
    TheHero["healthCur"] = 10
    TheHero["healthCap"] = 10
    TheHero["staminaCur"] = 8
    TheHero["staminaCap"] = 8
    TheHero["gold"] = 0
    TheHero["location"] = locations.ThePlains["name"]
    
    for key, value in TheHero["inventory"].items():
        value["name"] = "null"
    tools.saveInfo()
    return locations.ThePlains

def playerOptions(selected):
    if selected == "e":
        exit()
    elif selected == "o":
        displayPlayerInventory()
    elif selected == "p":
        input("status")
    else:
        return False
    return True

TheGameInfo = GameInfo(True)



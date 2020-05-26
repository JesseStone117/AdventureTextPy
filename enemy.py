# -*- coding: utf-8 -*-
"""
Created on Tue May 12 18:10:30 2020

@author: jesse
"""


import player
import tools
import equipment




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
    "loot": ["gold", 30]
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
    "loot": ["gold", 59]
}



def encounter(enemy):
    tools.clear()
    newEnemy = enemy.copy()
    
    if player.TheHero["speed"] > enemy["speed"]:
        action = "attack"
    else:
        action = "block"
    
    if action == "attack":
        print("\n"*7)
        print(tools.swordArt)
    else:
        print("\n"*7)
        print(tools.shieldArt)
        
    print("\n"*2, end="")
    input(" "*34 + "You've encountered a wild " + newEnemy ["name"] + ". Prepare to " + action + "!\n")
    
    while newEnemy ["healthCur"] > 0 and player.TheHero["healthCur"] > 0:
        if action == "attack":
            tools.attackBlock(newEnemy, action)
            action = "block"
        else:
            tools.attackBlock(newEnemy, action)
            action = "attack"
    
    if player.TheHero["healthCur"] < 1:
        return False
    
    player.acquireLoot(newEnemy)
    tools.clear()
    print("\n"*13, end="")









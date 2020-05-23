# -*- coding: utf-8 -*-
"""
Created on Tue May 12 18:10:30 2020

@author: jesse
"""


import player
import _thread
import tools
import equipment
from time import sleep

Null = {
    "name": "null",
    "healthCap": 0,
    "healthCur": 0,
    "strength": 0,
    "weapon": {"name": "null", "damage": 0},
    "speed": 0,
    "intelligence": 0,
    "loot": ["gold", 0]
}

Brownie = {
    "name": "brownie",
    "healthCap": 3,
    "healthCur": 3,
    "strength": 1,
    "weapon": equipment.Claws,
    "speed": 1,
    "intelligence": 1,
    "loot": ["gold", 9]
}

Goblin = {
    "name": "goblin",
    "healthCap": 4,
    "healthCur": 4,
    "strength": 2,
    "weapon": equipment.Dagger,
    "speed": 3,
    "intelligence": 2,
    "loot": ["gold", 30]
}


def attackInput(a_list):
    input()
    a_list.append(True)

# def displayActionBar():

def displayActionBar(enemy, action):
    a_list = []
    missBegOffset = "-"*20
    missEndOffset = "-"*5
    badOffset = "-"*12
    goodOffset = " "*6
    excellentOffset = "\|/"
    count = 0
    barOffset = " "*30
    progressSpeed = .011
    speedDiff = (player.TheHero["speed"] - enemy["speed"])/5000
    barLength = len(missBegOffset) + len(missEndOffset) + (2*len(badOffset)) + (2*len(goodOffset)) + len(excellentOffset)
    progression = barOffset + "█"
    rating = ["Failed", 0]
    
    badBeg = len(missBegOffset)
    goodBeg = badBeg+len(badOffset)
    excellentBeg = goodBeg+len(goodOffset)
    
    excellentEnd = goodBeg+len(goodOffset)+len(excellentOffset)
    goodEnd = excellentEnd+len(goodOffset)
    badEnd = goodEnd+len(badOffset)
    
    print("\n" + barOffset + missBegOffset + badOffset + goodOffset + excellentOffset + goodOffset + badOffset + missEndOffset)
    
    _thread.start_new_thread(attackInput, (a_list,))
    while not a_list and count < barLength:
        count += 1
        print(progression, end="\r")
        progression += "█"
        if action == "attack":    
            sleep(progressSpeed+speedDiff+player.TheHero["speed"]/1000)
        else:
            sleep(progressSpeed+(speedDiff*10)-enemy["speed"]/5000)
    
    if count < badBeg or count >= badEnd:
        rating = ["Failed", 0]
    
    if count > badBeg and count <= badEnd:
        if action == "attack":
            rating = ["Bad", .5]
        else:
            rating = ["Bad", .75]
        
    if count > goodBeg and count <= goodEnd:
        if action == "attack":
            rating = ["Good", 1]
        else:
            rating = ["Good", .25]
        
    if count > excellentBeg and count <= excellentEnd:
        if action == "attack":
            rating = ["Excellent", 1.5]
        else:
            rating = ["Excellent", 1]
    
    return rating
    
    # print("badBeg: "+str(badBeg))
    # print("badEnd: "+str(badEnd))
    
    # print("goodBeg: "+str(goodBeg))
    # print("goodEnd: "+str(goodEnd))
    
    # print("eBeg: "+str(excellentBeg))
    # print("eEnd: "+str(excellentEnd))

def attackBlock(enemy, action):
    attackSpacing = 22
    blockSpacing = 20
    rating = "Failed"
    
    tools.clear()
    
    print("\n"*3,end="")
    
    tools.displayHealth(player.TheHero)
    
    print("\n",end="")
    
    tools.displayHealth(enemy)
    
    if action == "attack":
        print("\n"+
          " "*attackSpacing + "_|_\n"+
          " "*attackSpacing + "|||\n"+
          " "*attackSpacing + "|||\n"+
          " "*attackSpacing + "|||\n"+
          " "*attackSpacing + "\|/",
          end = ""
        )
    else:
        print("\n"+
          " "*blockSpacing + " _____\n"+
          " "*blockSpacing + "|     |\n"+
          " "*blockSpacing + "| \\-/ |\n"+
          " "*blockSpacing + "|  |  |\n"+
          " "*blockSpacing + " \___/",
          end = ""
        )
    # print("\n"*13 + " "*64 + excellentOffsetTop)
    # print("\n"+" "*58+"count: "+str(count))
    rating = displayActionBar(enemy, action)
    
    print("\n"+" "*58+rating[0]+" "+action)
    
    if action == "attack":
        action = "block"
        enemy["healthCur"] -= player.TheHero["weapon"]["damage"]*rating[1]
    else:
        action = "attack"
        if enemy["healthCur"] > 0 and rating[0] != "Excellent":
            player.damagePlayer(enemy)
    
    if enemy["healthCur"] > 0:    
        print("\n" + " "*50 + "Now prepare to " + action + "!")
    else:
        print("\n" + " "*50 + "You have slain the " + enemy["name"] + "!")
    # if count < barLength:
    input()
    
    tools.clear()

def encounter(enemy):
    tools.clear()
    newEnemy = enemy.copy()
    attackSpacing = 22
    blockSpacing = 20
    
    if player.TheHero["speed"] > enemy["speed"]:
        action = "attack"
    else:
        action = "block"
    
    
    if action == "attack":
        print("\n"*7+
          " "*attackSpacing + "_|_\n"+
          " "*attackSpacing + "|||\n"+
          " "*attackSpacing + "|||\n"+
          " "*attackSpacing + "|||\n"+
          " "*attackSpacing + "\|/"
        )
    else:
        print("\n"*7+
              " "*blockSpacing + " _____\n"+
              " "*blockSpacing + "|     |\n"+
              " "*blockSpacing + "| \\-/ |\n"+
              " "*blockSpacing + "|  |  |\n"+
              " "*blockSpacing + " \___/"
        )
        
    print("\n"*2, end="")
    print(" "*34 + "You've encountered a wild " + newEnemy ["name"] + ". Prepare to " + action + "!\n")
        
    input()
    
    # if newEnemy["intelligence"] < player.TheHero["intelligence"]: # UNFINISHED, working on list (5/15, 11:19)
        # newEnemy["health"] -= player
    while newEnemy ["healthCur"] > 0 and player.TheHero["healthCur"] > 0:
        if action == "attack":
            attackBlock(newEnemy, action)
            action = "block"
        else:
            attackBlock(newEnemy, action)
            action = "attack"
        
    player.acquireLoot(newEnemy)
    tools.clear()
    print("\n"*13, end="")









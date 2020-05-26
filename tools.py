# -*- coding: utf-8 -*-
"""
Created on Tue May 12 17:25:21 2020

@author: jesse
"""
import os
import player
import locations
import base64
import _thread
from time import sleep

clear = lambda: os.system('cls') #on Windows System

os.system('mode con: cols=124 lines=30')

attackSpacing = 18
blockSpacing = attackSpacing-2

swordArt = (
          " "*attackSpacing + "_|_\n"+
          " "*attackSpacing + "|||\n"+
          " "*attackSpacing + "|||\n"+
          " "*attackSpacing + "|||\n"+
          " "*attackSpacing + "\|/"
)

shieldArt = (
              " "*blockSpacing + " _____\n"+
              " "*blockSpacing + "|     |\n"+
              " "*blockSpacing + "| \\-/ |\n"+
              " "*blockSpacing + "|  |  |\n"+
              " "*blockSpacing + " \___/"
)

def displayHealth(entity):
    healthBar = ""
    missingHealth = entity["healthCap"] - entity["healthCur"]
    remainingHealth = entity["healthCap"] - missingHealth
    
    name = entity["name"][0].upper()
    name += entity["name"][1:]
    
    # print(missingHealth)
    
    filledSegment = "██"*int(remainingHealth)
    emptySegment = "░░"*int(missingHealth)
    healthBar = emptySegment + filledSegment
    
    print("\n" + " "*(114-len(name)-(entity["healthCap"]*2)) + name + " Health: ", end="")
    
    print(healthBar,end="")

def damageEntity(entity, attacker, rating):
    # if entity["name"] != player.TheHero["name"]:
        # rating = 1
    
    weaponWeight = attacker["weapon"]["weight"]
    weaponDamage = attacker["weapon"]["damage"]
    attackerStrength = attacker["strength"]
    attackerDamage = weaponDamage + (attackerStrength - weaponWeight)/10
    # print((attackerStrength - weaponWeight)/10)
    attackerDamage *= rating
    # print("entity:",entity["name"],"\nattacker:",attacker["name"],"\ntotal Damage:",attackerDamage)
    attackerDamage = round(attackerDamage)
    currentHealth = entity["healthCur"] 
    currentHealth -= (attackerDamage-damageNegation(entity))
    
    if currentHealth < 0:
        currentHealth = 0
    
    entity["healthCur"] = currentHealth
    
    # print("entity:",entity["name"],"\nattacker:",attacker["name"],"\ntotal Damage:",attackerDamage)
    saveInfo()
    
def damageNegation(entity):
    negatedDamage = 0
    
    if entity["armor"] >= 10:
        negatedDamage = 1
    
    return negatedDamage

def attackInput(a_list):
    input()
    a_list.append(True)

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
    
    barVisual = "\n" + barOffset + missBegOffset + badOffset + goodOffset + excellentOffset + goodOffset + badOffset + missEndOffset
    
    print(barVisual)
    
    for x in range(4):
        print(" "*(53-len(action)) + action[0].upper() + action[1:] + "ing in: " + str(abs(x-3)),end="\r")
        sleep(.17)
    
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
        if action == "attack":
            rating = ["Failed", 0]
        else:
            rating = ["Failed", 1]
    
    if count > badBeg and count <= badEnd:
        if action == "attack":
            rating = ["Bad", .5]
        else:
            rating = ["Bad", .75]
        
    if count > goodBeg and count <= goodEnd:
        if action == "attack":
            rating = ["Good", 1]
        else:
            rating = ["Good", .50]
        
    if count > excellentBeg and count <= excellentEnd:
        if action == "attack":
            rating = ["Excellent", 1.5]
        else:
            rating = ["Excellent", 0]
    
    if action == "attack":
        damageEntity(enemy, player.TheHero, rating[1])
    else:
        damageEntity(player.TheHero, enemy, rating[1])
    
    attackBlockResults(rating[0], action, rating[1], enemy, barVisual, barOffset, count)
    
    return rating
    
    # print("badBeg: "+str(badBeg))
    # print("badEnd: "+str(badEnd))
    
    # print("goodBeg: "+str(goodBeg))
    # print("goodEnd: "+str(goodEnd))
    
    # print("eBeg: "+str(excellentBeg))
    # print("eEnd: "+str(excellentEnd))

def attackBlock(enemy, action):
    clear()
    
    print("\n"*3,end="")
    
    displayHealth(player.TheHero)
    
    print("\n",end="")
    
    displayHealth(enemy)
    
    if action == "attack":
        print("\n")
        print(swordArt)
    else:
        print("\n")
        print(shieldArt)
    
    displayActionBar(enemy, action)
    
    if action == "attack":
        action = "block"
    else:
        action = "attack"
    
    if enemy["healthCur"] > 0:
        input("\n" + " "*50 + "Now prepare to " + action + "!")
    else:
        input("\n" + " "*50 + "You have slain the " + enemy["name"] + "!")
    
def attackBlockResults(ratingText, action, ratingValue, enemy, barVisual, barOffset, count):
    clear()
    
    print("\n"*3,end="")
    
    displayHealth(player.TheHero)
    
    print("\n",end="")
    
    displayHealth(enemy)
    
    if action == "attack":
        print("\n")
        print(swordArt)
    else:
        print("\n")
        print(shieldArt)
    
    print(barVisual)
    print(barOffset + "█"*count)
    
    print("\n"+" "*58+ratingText+" "+action)

def loadInfo():
    try:
        f = open("playerInfo.sav", "r")
    except:
        f = open("playerInfo.sav", "w")
        
        playerInfo = str(player.TheHero)
        playerInfoBytes = playerInfo.encode('ascii')
        base64Bytes = base64.b64encode(playerInfoBytes)
        base64playerInfo = base64Bytes.decode('ascii')
        
        f.write(base64playerInfo)
        
        f.close()
        
        return locations.ThePlains
        
    else:
        playerInfo = f.read()
        playerInfoBytes = playerInfo.encode('ascii')
        base64Bytes = base64.b64decode(playerInfoBytes)
        base64playerInfo = base64Bytes.decode('ascii')
        
        player.TheHero = eval(base64playerInfo)
        
        f.close()
        
        count = 0
        for x in locations.Areas:
            if player.TheHero["location"] == locations.Areas[count]["name"]:
                return locations.Areas[count]
            count += 1
        
        return locations.ThePlains

def saveInfo():
    f = open("playerInfo.sav", "w")
    
    playerInfo = str(player.TheHero)
    playerInfoBytes = playerInfo.encode('ascii')
    base64Bytes = base64.b64encode(playerInfoBytes)
    base64playerInfo = base64Bytes.decode('ascii')
    
    f.write(base64playerInfo)
    
    f.close()









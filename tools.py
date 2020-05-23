# -*- coding: utf-8 -*-
"""
Created on Tue May 12 17:25:21 2020

@author: jesse
"""
import os
import player
import locations
import base64

clear = lambda: os.system('cls') #on Windows System

os.system('mode con: cols=124 lines=30')

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









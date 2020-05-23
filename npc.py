# -*- coding: utf-8 -*-
"""
Created on Wed May 13 16:15:38 2020

@author: jesse
"""

import tools
import player
import items

TheShopkeep = {
    "name": "Burrel",
    "healthCap": 20,
    "healthCur": 20,
    "strength": 2,
    "weapon": ["claws", 1],
    "wares": [items.smallHealthPotion, items.smallLoafOfBread],# items.mediumHealthPotion, items.freshCherryPie],
    "speed": 1,
    "loot": ["gold", 9]
}

TheShadowMan = {
    "name": "Shadow Man",
    "healthCap": 30,
    "healthCur": 30,
    "strength": 2,
    "weapon": ["claws", 1],
    "speed": 1,
    "loot": ["gold", 9]
}

def talkToTheShopkeep():
    selected = 0
    status = []
    conversing = True
    shopping = False
    heroTalking = "\n  " + player.TheHero["name"] + ": " 
    shopkeepTalking = "\n  " + TheShopkeep["name"] + ": "
    tools.clear()
    
    selected = input("\n" *3 + shopkeepTalking + "Hello, could I interest you in some wares?").lower()
    
    while conversing:
        if shopping == False:
            selected = input(
                "\n  [1] Browse the shopkeep's wares"+
                " | [2] Ask about the shadow man"+
                " | [E]nd conversation\n    Say: "
            ).lower()
        else:
            print(
                "\n  [1] Browse the shopkeep's wares"+
                " | [2] Ask about the shadow man"+
                " | [E]nd conversation\n    Say: " + selected
            )
            selected = "1"
        
        if selected == "1":
            player.displayGold()
            status = displayShopkeepSelection()
            
            if status[0] == True:
                shopping = True
            else:
                shopping = False
                selected = "e"
                
            if status[1] == True:
                conversing = True
            else:
                conversing = False
                selected = "e"
                
        elif selected == "2":
            dialogue(heroTalking, "What can you tell me about the shadow man?")
            
            dialogue(
                shopkeepTalking, "Ah, a real cook that one. Claims he used to live among The Derelict.\n",
                "I wouldn't trust anything he has to say."
            )
                
        elif selected == "e":
            conversing = False
            
            dialogue(heroTalking, "Farewell.")
            
            dialogue(shopkeepTalking, "Comeback soon!")

        else:
            input("  Invalid selection...")
            
        tools.clear()
        print("\n" *3 + shopkeepTalking + "Hello, could I interest you in some wares?")

def displayShopkeepSelection():
    # tools.clear()
    conversing = True
    shopping = True
    goodSelect = False
    output = "\n"
    cellLength = 30
    tableCentering = 40
    
    print()
    
    for objects in TheShopkeep["wares"]:
        print(
            " "*tableCentering + "-"*cellLength + "\n" + " "*tableCentering +
            "|  " + objects["name"] + " "*(26-len(objects["name"])) + "|  " + str(objects["cost"]) + " gold"
            )
        
    print(" "*tableCentering + "-"*30 + "\n")
    
    for idx, item in enumerate(TheShopkeep["wares"]):
        if idx == 0:
            output += "  [" + str(idx+1) + "] Purchase"
            
        elif idx == 3:
            output += " [" + str(idx+1) + "] Purchase"
            
        else:
            output += " | [" + str(idx+1) + "] Purchase"
            
        output += TheShopkeep["wares"][idx]["name"]
        
        if idx == 2:
            output += "\n   "
    
    output += " | [E]nd conversation\n\n    I want to: "
    
    selected = input(output)
    
    for idx, item in enumerate(TheShopkeep["wares"]):
        if selected == str(idx+1):
            player.purchaseItem(TheShopkeep["wares"][idx])
            goodSelect = True
    
    if goodSelect == False:
        if selected == "e":
            conversing = False
            return [shopping, conversing]
        else:
            input("  Invalid selection...")
    
    return [shopping, conversing]
        
    
def talkToShaymus():
    selected = 0
    conversing = True
    heroTalking = "\n  " + player.TheHero["name"] + ": " 
    shaymusTalking = "\n  Shaymus: "
    tools.clear()
    
    selected = input("\n" *3 + shaymusTalking + "Well hello there laddy!").lower()
    
    while conversing:
        selected = input(
            "\n  [1] Comment on his height"+
            " | [E]nd conversation\n    Say: "
        )
        
        # selected = verification(selected, 2)
        
        if selected == "1":
            dialogue(heroTalking, "You're tall for a leprechaun.")
            
            dialogue(shaymusTalking, "I'LL PUT YA IN THE CUBBARD.")
            
        elif selected == "e":
            conversing = False
            
            dialogue(heroTalking, "Farewell.")
            
            dialogue(shaymusTalking, "Oi!")

        else:
            input("  Invalid selection...")
            
        tools.clear()
        print("\n" *3 + shaymusTalking + "Well hello there laddy!")

def talkToTheShadowMan():
    selected = 0
    conversing = True
    heroTalking = "\n  " + player.TheHero["name"] + ": " 
    shadowManTalking = "\n  The Shadow Man: "
    tools.clear()
    
    input("\n" *3 + shadowManTalking + "Yes, what would you ask of me?")
    
    while conversing:
        selected = input(
            "\n  [1] Ask about his name"+
            " | [2] Ask about The Deep"+
            " | [3] Ask about his strange weapon"+
            " | [E]nd conversation\n    Say: "
        ).lower()
        
        # selected = verification(selected, 4)
        
        if  selected == "1":
            dialogue(heroTalking, "Why do they call you the Shadow Man?")
            
            dialogue(shadowManTalking, "I could explain that to you, but you would not understand it.")
            
            dialogue(heroTalking, "Wow.. well that's ominous")
        
        elif selected == "3":
            dialogue(heroTalking, "Hey cool weapon.")
            
            dialogue(shadowManTalking, "Uh, thanks.")
            
            dialogue(heroTalking, "You're welcome!")
        
        elif selected == "e":
            conversing = False
            
            dialogue(heroTalking, "Farewell.")
            
            dialogue(shadowManTalking, "Until next time, traveler.")
        
        elif selected == "2":
            dialogue(heroTalking, "Tell about The Deep?")
            
            dialogue(
                shadowManTalking, "Ahh yes, The Deep. It is the harrowing abyss. The endless peril of The Lost.\n",
                "It is a place of nightmares. A place of no return...\""
            )
            
            selected = input(
                "\n  [1] Express fear"+
                " | [2] Express interest"+
                " | [3] Ask about The Lost\n    Say: "
            )
            
            selected = verification(selected, 3)
            
            if int(selected) == 1:
                dialogue(heroTalking, "I think I'll stay away...")
                
                dialogue(shadowManTalking, "A wise decision indeed.")
                
            if int(selected) == 2:
                dialogue(heroTalking, "Well now I have to check it out...")
                
                dialogue(shadowManTalking, "A foolish sentiment to be sure. But if that is your decision, at least take this with you.")
                
                
            if int(selected) == 3:
                dialogue(heroTalking, "You mentioned The Lost? Who are they? Can you tell me about them?")
                
                dialogue(
                    shadowManTalking, "Not they. Not them. Not him or her. The Lost is a presence older than time.\n",
                    "A magnificent creation hastily abondoned, though not without reason. Without shape or form.\n",
                    "You would be wise to banish the name from your mind."
                )
                
                dialogue(heroTalking, "Um, I see... Forget I asked.")
        else:
            input("  Invalid selection...")
            
        tools.clear()
        print("\n" *3 + shadowManTalking + "Yes, what would you ask of me?")

def verification(selected, options):
    try:
        selected = int(selected)
        if selected <= 0 or selected > options:
            input("  Invalid selection...")
            selected = 0
    except:
        selected = 0
        if selected <= 0 or selected > options:
            input("  Invalid selection...")
            
    return selected

def dialogue(speaker, *speech):
    count = 0
    # thing = " "*(len(speaker)+1)
    
    finishedText = speaker
    finishedText += "\""
    for x in speech:
        if count == 0 or len(speech) == 1:
            finishedText += x
        else:
            finishedText += " "*(len(speaker)+count)
            finishedText += x
        count += 1
        
    finishedText += ("\"")
    input(finishedText)



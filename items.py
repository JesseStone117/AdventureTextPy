# -*- coding: utf-8 -*-
"""
Created on Fri May 22 11:49:15 2020

@author: jesse
"""

null = {
    "name": "null",
    "weight": 0,
    "cost": 0,
    "effect": ["null", 0]
}

caveOfDarkMap = {
    "name": "Cave of Dark Map",
    "weight": 1,
    "cost": 100,
    "effect": ["map", 0],
    "use": "dungeons.displayCaveOfDarkMap()"
}

sunkenCitadelMap = {
    "name": "Sunken Citadel Map",
    "weight": 1,
    "cost": 100,
    "effect": ["map", 0],
    "use": "dungeons.displaySunkenCitadelMap()"
}

smallLoafOfBread = {
    "name": "Small Loaf of Bread",
    "weight": 1,
    "cost": 3,
    "effect": ["stamina", 4],
    "use": "useFood(items.smallLoafOfBread)"
}

freshCherryPie = {
    "name": "Fresh Cherry Pie",
    "weight": 2,
    "cost": 8,
    "effect": ["stamina", 8],
    "use": "useFood(items.freshCherryPie)"
}

smallHealthPotion = {
    "name": "Small Health Potion",
    "weight": 2,
    "cost": 4,
    "effect": ["health", 2],
    "use": "usePotion(items.smallHealthPotion)"
}

mediumHealthPotion = {
    "name": "Medium Health Potion",
    "weight": 3,
    "cost": 6,
    "effect": ["health", 4],
    "use": "usePotion(items.mediumHealthPotion)"
}

largeHealthPotion = {
    "name": "Large Health Potion",
    "weight": 4,
    "cost": 10,
    "effect": ["health", 8],
    "use": "usePotion(items.largeHealthPotion)"
}

ultraHealthPotion = {
    "name": "Ultra Health Potion",
    "weight": 6,
    "effect": ["health", 12],
    "use": "usePotion(items.ultraHealthPotion)"
}

# elixir = {
#     "name": "Elixir",
#     "weight": 10,
#     "effect": ["mult", 0],
#     "effects": [freshCherryPie, largeHealthPotion]
# }

potionOfAscendance = {
    "name": "Potion Of Ascendance",
    "weight": 2,
    "cost": 999,
    "effect": ["ascend", 0],
    "use": "ascend(items.potionOfAscendance)"
}


def getItemUsage(item):
    usage = ""

    if item["effect"][0] == "health" or item["effect"][0] == "stamina":
        usage += "(restores " + str(item["effect"][1]) + " " + item["effect"][0] + ")"

    # elif item["effect"][0] == "ascend":
    # usage = "* Soul Bound *"

    return usage

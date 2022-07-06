# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 19:36:03 2020

@author: jesse
"""

import locations
import tools
import player
import random
import time
import items

# def restart():
#     os.execv(sys.executable, ['main'] + sys.argv)

def main():
    random.seed(str(time.time))
    inMenu = True

    # player.acquireItem(items.sunkenCitadelMap)
    # player.acquireItem(items.caveOfDarkMap)
    # player.acquireItem(items.potionOfAscendance)

    while inMenu:
        inMenu = tools.displayMainMenu()

        inGame = True

        while inGame:
            inGame = locations.processAreaOptions()
            if player.TheHero["healthCur"] < 1:
                player.deathProcess()


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 19:36:03 2020

@author: jesse
"""

import locations
import random
import time
import tools
import player

def main():
    random.seed(time.time)
    tools.clear()
    location = tools.loadInfo()
    
    input("\n\n\n Welcome back traveler. Press enter to resume your adventure...")
    tools.clear()
    
    while True:
        location = locations.displayAreaOptions(location)
        if player.TheHero["healthCur"] < 1:
            location = player.deathProcess()
            
if __name__ == "__main__":
    main()
import numpy as np
#Map Design: 1's are dungeon walls, 0 is space one can travel to.
dungeonMap = np.full((6, 7), 0) #Creating the board
#Outer walls
dungeonMap[0:, 0] = 1
dungeonMap[0, 0:] = 1
dungeonMap[5, 0:] = 1
dungeonMap[0:, 6] = 1
#Inner Walls
dungeonMap[0:4, 2] = 1 #Column 2
dungeonMap[1, 4] = 1
dungeonMap[3:5, 4] = 1

#Stuff on the map
dungeonMap[1, 1] = 2 #Spawn
dungeonMap[3, 1] = 3 #First item pickups
dungeonMap[3, 3] = 4 #Skeleton
dungeonMap[1, 3] = 5 #chest
dungeonMap[4, 2] = 6 #Giant Spider
dungeonMap[4, 1] = 7 #Setting the scene: Spiders
dungeonMap[2, 4] = 8 #Gargoyle
dungeonMap[1, 5] = 9 #Final Boss
dungeonMap[4, 5] = 10 #End of the game
dungeonMap[1, 2] = 11 # Giant rat
dungeonMap[3, 5] = 12 #Sorcerer
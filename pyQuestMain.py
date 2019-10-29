# Dependencies
import random
import pyQuestMap
import numpy as np
import pandas as pd
from collections import Counter
import pyfiglet

# Global Variables
global dead
dead = False
global health
health = 100
global name
global isAtEnd
isAtEnd = False

# Variables
map = pyQuestMap.dungeonMap
inventory = ["Torch"]
x = 1
y = 1
coordinates = [x, y]
position = map[coordinates]

# The list of moves, stored in a dictionary.
moves = {
    "move": "'move [direction]'. This will move you one space in the direction you specify. ex: 'move west'",
    "map": "Displays the map",
    "drink": "Drinks a health potion.",
    "inventory": "Views your inventory.",
    "health": "Shows your health",
    "drink": "Drinks a health potion (+30 hp)",
    "exit": "Exit PyQuest."
}


def drink(inventory, health):
    try:
        if health == 100:
            print("Your health is full, no need to drink!")

        elif health <= 70:
            health = health + 30
            inventory.remove("Health Potion")
            print("You pull out a health potion from your inventory, and drink its continents.")
            print("You healed for 30 Health.")
            print("Your health is now: " + str(health) + ".")

        elif health > 70:
            health = 100
            inventory.remove("Health Potion")
            print("You pull out a health potion from your inventory, and drink its continents.")
            print("Your health is now: " + str(health) + ".")
    except ValueError:
        print("There are 0 Health Potions in your inventory.")

"""Function To show your available moves in explore mode. This function prettifies the printing of the move list."""


def showMoveList():
    for key, value in moves.items():
        print(key + " -> " + value + "\n")


"""Function to show the player's inventory.the collections package has a counter method to count the items in 
 the player's inventory. """


def showInventory(inventory):
    itemList = dict(Counter(inventory))
    return itemList


"""This is the basic combat system for PyQuest.  The adventurer has three different moves they can do while in the 
combat 'state'. """


def combat(playerHealth, playerInventory, playerName, npcHealth, npcName):
    while playerHealth > 0 and npcHealth > 0:
        npcAttack = random.randint(20, 30)
        global dead
        global health
        health = playerHealth
        isDefending = False

        combatCommand = input("What is your move? ('attack', 'defend', 'drink') :")
        combatCommand = combatCommand.lower()
        # Attacking the enemy
        if "attack" in combatCommand:
            print("You strike the " + npcName + "!")
            # Critical strike
            critRoll = random.randint(0, 10)
            if critRoll >= 8:
                print("Critcal strike!")
                dmg = random.randint(20, 40)
            else:
                dmg = random.randint(1, 20)
            npcHealth = npcHealth - dmg
            if npcHealth <= 0:
                print("You have defeated the " + npcName + "!")
                health = playerHealth
                return True
            print("You did " + str(dmg) + " damage to " + npcName)
            print("The " + npcName + " has " + str(npcHealth) + " health left.")
            # The NPC can also critically strike the player.
            npcCritRoll = random.randint(0, 10)
            if npcCritRoll >= 8:
                npcAttack = random.randint(10, 20)
                print("The " + npcName + " critcally strikes you!")
            else:
                npcAttack = random.randint(0, 10)
            playerHealth = playerHealth - npcAttack
            print("The " + npcName + " attacked you for " + str(npcAttack) + " damage.")
            print(npcName + "'s health is now " + str(npcHealth))
            print("Your health is now " + str(playerHealth))
            if playerHealth <= 0:
                print("You suffer a horrifying death at the hands of the " + npcName + ".")
                print("The journey of " + playerName + " has ended.")
                dead = True
                return False

        # Defending allows you to take LESS damage from the next enemy attack, and return a weaker attack.
        if "defend" in combatCommand:
            print("You hold your shield, anticipating the opponent's attack...")
            npcAttack = random.randint(0, 10)
            playerHealth = playerHealth - (.5 * npcAttack)
            print(npcName + " attacked you for " + str((.5 * npcAttack)) + " damage." + " Your health is now " + str(
                playerHealth))
            if playerHealth <= 0:
                print("You suffer a horrifying death at the hands of the " + npcName + ".")
                print("The journey of " + playerName + " has ended.")
                dead = True
                return False
            print("You strike the " + npcName + "!")
            # Critical strike
            critRoll = random.randint(0, 10)
            if critRoll >= 8:
                print("Critcal strike!")
                dmg = random.randint(5, 10)
            else:
                dmg = random.randint(0, 5)
            npcHealth = npcHealth - dmg
            if npcHealth <= 0:
                print("You have defeated the " + npcName + "!")
                health = playerHealth
                return True
            print("You did " + str(dmg) + " damage to " + npcName)
            print("The " + npcName + " has " + str(npcHealth) + " health left.")

        # Drink allows you to drinlk without taking damage.
        if "drink" in combatCommand:
            drink(playerInventory, playerHealth)


"""Function to show the map in explore mode. Since the map is a numpy array, it requires some beautification to fit 
the dungeon theme better. """


def showMap():
    # Replacing everything other than walls with a question mark, because you can't see very well in the dark dungeon.
    emptyMap = np.where(map > 2, '?', map)
    # Changing the data type of the variables in the array to a string (this way we have more options for cool ASCII characters.)
    tmpMap = np.array(emptyMap, dtype='str')
    # Changing the walls into 'blocks'.
    walls = np.where(tmpMap == '1', '█', tmpMap)
    # Replacing the blank spaces (0's originally) into empty space.
    spaces = np.where(walls == '0', ' ', walls)
    # Replacing the character(Value of 2) into an ASCII smiley face.
    you = np.where(map == 2, "☺", spaces)
    # Converting the array into a pandas dataframe and removing the indexes to get rid of some of python's data structure formatting.
    beautified = pd.DataFrame(you)
    print(beautified.to_string(index=False, header=False))


"""Function that triggers events based on where the character is on the map. It will take the numerical value of the 
coordinate you are in, and then based on said coordinate, different events will trigger. """


def eventAtPosition(newCoords, oldCoords):
    # Slicing the string and storing only the coordinates.
    newCoordString = str(newCoords)
    oldCoordString = str(oldCoords)
    newCoordinates = list(filter(lambda coord: coord.isdigit(), newCoordString))
    oldCoordinates = list(filter(lambda coord: coord.isdigit(), oldCoordString))

    # Preventing the character from running through walls. 1's are walls in the array.
    if map[int(newCoordinates[0]), int(newCoordinates[1])] == 1:
        print("You tried to move, but in the darkness you felt a dungeon wall upon moving.")
        map[int(newCoordinates[0]), int(newCoordinates[1])] = 1
        map[int(oldCoordinates[0]), int(oldCoordinates[1])] = 2
        return False

    # Early game potion chest
    if map[int(newCoordinates[0]), int(newCoordinates[1])] == 3:
        print("As you walk along the hallway, you stumble upon a small wooden chest on the ground.")
        print("Intrigued, you pick the box up and notice there is some heft to it, something must be inside...")
        boxOption = input("Do you open the box? 'yes' or 'no'. :")
        boxOption = boxOption.lower()

        # Do you open the chest?
        if "no" in boxOption:
            print("You gently put the box down, and take a step back.")
            map[int(newCoordinates[0]), int(newCoordinates[1])] = 3
            map[int(oldCoordinates[0]), int(oldCoordinates[1])] = 2
            return False
        else:
            print("A spider crawls out of the box")
            print("In shock, you abruptly drop the box, damaging its wooden frame.")
            print("In the destruction you notice three health potions.")
            print("3 Health Potion(s) added to your inventory.")
            inventory.append("Health Potion")
            inventory.append("Health Potion")
            inventory.append("Health Potion")
        # You take the spiders place, the new space is a 0.
        map[int(newCoordinates[0]), int(newCoordinates[1])] = 2
        map[int(oldCoordinates[0]), int(oldCoordinates[1])] = 0
        return True

    # Skeleton Encounter.
    elif map[int(newCoordinates[0]), int(newCoordinates[1])] == 4:
        print("As you take your next step, you hear something rattling a few feet away from you.")
        print("You bring your torch up to the direction where you heard the rattling.")
        print("Upon further inspection, you notice a pile of bones reforming itself into a human skeleton.")
        print("The skeleton reaches for a nearby sword, and you draw yours...")
        print("You are in combat!")

        # If the skeleton kills you, game over.
        if not combat(health, inventory, name, 75, "Skeleton"):
            dead = True
            return False


        # If you kill the skeleton, you progress and move to his position successfully.
        else:
            map[int(newCoordinates[0]), int(newCoordinates[1])] = 2
            map[int(oldCoordinates[0]), int(oldCoordinates[1])] = 0
            print("The skeleton dropped a Health Potion")
            inventory.append("Health Potion")
            return True
    # Glamerous treasure chest, contains a lot of health potions.
    if map[int(newCoordinates[0]), int(newCoordinates[1])] == 5:
        print("You encounter a treasure chest, with a beam of light illuminating it from a gap in the dungeon's walls.")
        print("No signs of blood, spiders, or dark magic.")
        chestOption = input("Do you open the chest? 'yes' or 'no' :")
        #Do you open the chest?
        if "no" in chestOption:
            print("You step away from the chest.")
            map[int(newCoordinates[0]), int(newCoordinates[1])] = 5
            map[int(oldCoordinates[0]), int(oldCoordinates[1])] = 2
            return False

        else:
            print("3 Health Potion(s) added to your inventory.")
            inventory.append("Health Potion")
            inventory.append("Health Potion")
            inventory.append("Health Potion")
            map[int(newCoordinates[0]), int(newCoordinates[1])] = 2
            map[int(oldCoordinates[0]), int(oldCoordinates[1])] = 0
            return True
    #Spider fight.
    elif map[int(newCoordinates[0]), int(newCoordinates[1])] == 6:
        print("You find it harder to move as you take your next step.")
        print("You lower your torch to reveal a large silk web, revealing movement in the darkness approaching you.")
        print("As it gets closer, you notice it is a giant spider, its fangs are the size of daggers.")
        print("You draw out your sword.")
        print("You are in combat!")
        # If the spider kills you, game over.
        if not combat(health, inventory, name, 75, "Spider"):
            dead = True
            return False

        # If you kill the spider, you progress and move to his position successfully.
        else:
            map[int(newCoordinates[0]), int(newCoordinates[1])] = 2
            map[int(oldCoordinates[0]), int(oldCoordinates[1])] = 0
            print("The spider dropped a Health Potion!")
            inventory.append("Health Potion")
            return True
        #Non combat event, warning you that combat is near.
    elif map[int(newCoordinates[0]), int(newCoordinates[1])] == 7:
        print("You notice hundreds of small spiders crawling along the dungeon walls.")
        print("Cautiously, you firmly grip your torch and keep your hand on your sword, ready to draw.")
        map[int(newCoordinates[0]), int(newCoordinates[1])] = 2
        map[int(oldCoordinates[0]), int(oldCoordinates[1])] = 0
        return True

    # An optional Gargoyle fight
    elif map[int(newCoordinates[0]), int(newCoordinates[1])] == 8:
        print("A large gargoyle blocks your path.")
        print(
            "You notice the gargoyle has a small opening in its hand, perfectly shaped to fit the handle of your sword. ")
        garGoyleOption = input("Do you put your sword in the gargoyle's hand?")
        garGoyleOption = garGoyleOption.lower()
        #If you don't give him your sword, he fights you.
        if "no" in garGoyleOption:
            print("You notice the stat slowly coming to life...")
            print("It locks eyes with you...")
            print("'You have made a grave mistake!'")
            print("The gargoyle charges at you.")
            print("You draw your sword.")
            print("You are in combat!")
            map[int(newCoordinates[0]), int(newCoordinates[1])] = 2
            map[int(oldCoordinates[0]), int(oldCoordinates[1])] = 0
            if not combat(health, inventory, name, 100, "Gargoyle"):
                dead = True
                return False

        #If you give him your sword, he is delighted by your kindness and doesn't fight you.
        else:
            print("You notice the stat slowly coming to life...")
            print("It locks eyes with you...")
            print(
                "'Thank you. I am not sure how long I have been sleeping here! But I have important matters to attend to.'")
            print("In gargoyle code, it is considered respectful to offer your weapon in good faith.")
            print(
                "'There is a treasure chest around here full of my potions. Please take them. Evil lurks beyond this point. '")
            print("'And I almost forgot, you will be needing this!")
            print("The gargoyle returns your sword.")
            print("The gargoyle walks away, vanishing into the darkness.")
            map[int(newCoordinates[0]), int(newCoordinates[1])] = 2
            map[int(oldCoordinates[0]), int(oldCoordinates[1])] = 0
            return True
    # Dragon Fight
    elif map[int(newCoordinates[0]), int(newCoordinates[1])] == 9:

        print("As you take your next step, you notice the earth around you shaking.")
        print("The structural integrity of the dungeon is failing!")
        print("Cracks in the floors begin emerging followed by dungeon walls collapsing.")
        print("The destruction of the dungeon seems to be following a pattern, it's almost rhythmic.")
        print("The entire floor collapses!")
        print("A dragon bursts through the floor, it's bigger than ten castles!")
        print("Its fangs are longer than your sword, its claws are bigger than a horse.")
        print("The dragon viciously roars in your face.")
        print("You draw your sword and grip it with all of your might.")
        print("You are in combat!")
        # If the dragon kills the player, the game is over.
        if not combat(health, inventory, name, 150, "Dragon"):
            dead = True
            return False
        # If the player survives, they may continue.
        else:
            print(
                "The dragon collapses into the ground, bursting into a flame brighter than the sun, blinding your vision.")
            print("You notice a distinct clanking noise after the dragon was defeated.")
            print("As your vision comes to, you notice a key larger than you've ever seen before.")
            print("You take the key, and toss it over your back.")
            inventory.append("Dragon Key")
            map[int(newCoordinates[0]), int(newCoordinates[1])] = 2
            map[int(oldCoordinates[0]), int(oldCoordinates[1])] = 0
            return True
    #End of the game, exit to dungeon
    elif map[int(newCoordinates[0]), int(newCoordinates[1])] == 10:
        print(
            "As you reach the end of the hallway, you notice a massive threshold. with a large key hole in the middle.")
        print("It is bound by some type of dark magic, there is no way to open it without a massive key.")
        # If the player has the dragon key, they may end the game.
        if "Dragon Key" in inventory:
            global isAtEnd
            isAtEnd = True
            map[int(newCoordinates[0]), int(newCoordinates[1])] = 2
            map[int(oldCoordinates[0]), int(oldCoordinates[1])] = 0
            print("You enter through the threshold into a bright room, overlooking your city!")
            print("You notice  see the destruction and devastation that the dungeon has released into the world has "
                  "been vanquished.")
            print(name + ", You have done a great deed!")
            print("You saved the world from chaos and destruction!")
            print("There will be statues of you, books written about your might and triumph!")
            print("You escape the dungeon, being praised by the entire town and a festival is thrown in your honor.")
            print("You meet the love of your life, have  children, and live out the rest of your days as a hero.")
            print("Thank you for playing PyQuest!")
            endText = pyfiglet.figlet_format("The End")
            print(endText)
            return True

        # If the player reaches the end without the key, they may not pass.
        else:
            print("A magical key is required to get through.")
            map[int(newCoordinates[0]), int(newCoordinates[1])] = 10
            map[int(oldCoordinates[0]), int(oldCoordinates[1])] = 2
            return False

    # Giant rat fight
    elif map[int(newCoordinates[0]), int(newCoordinates[1])] == 11:
        print("In the darkness, you notice a high pitched squeaking noise...")
        print("As you put your torch ahead you see a blur of movement ahead, no bigger than a dog.")
        print("Upon deeper investigation you notice the blur being 'rodent' shaped.")
        print("The giant rodent becomes startled by your presence...")
        print("The rodent charges at you!")
        print("You draw your sword...")
        print("You are in combat!")
        # If the rat kills the player, game over.
        if not combat(health, inventory, name, 20, "Rat"):
            dead = True
            return

        # If you kill the rat, you progress and move to his position successfully.
        else:
            map[int(newCoordinates[0]), int(newCoordinates[1])] = 2
            map[int(oldCoordinates[0]), int(oldCoordinates[1])] = 0
            print("You search through the rodent's nest and find a health potion!")
            inventory.append("Health Potion")
            return True
    # Sorcerer, final boss
    elif map[int(newCoordinates[0]), int(newCoordinates[1])] == 12:
        print("You encounter a sorcerer, enraged that you dare disturb his experiments in the dungeon.")
        print("'You fool! you will pay for this.'")
        print("No one enters my dungeon and distrupts my experiments without suffering!")
        print("The sorcerer casts a fire spell and hurls it at you!")
        print("You block it with your shield!")
        print("You draw your sword!")
        print("You are in combat!")
        if not combat(health, inventory, name, 250, "Sorcerer"):
            dead = True
            return
        else:
            map[int(newCoordinates[0]), int(newCoordinates[1])] = 2
            map[int(oldCoordinates[0]), int(oldCoordinates[1])] = 0
            print("As the sorcerer falls to his death, you notice a great threshold ahead.")
            return True

    # The character moves somewhere and nothing interesting takes place on that point on the map.
    else:
        map[int(newCoordinates[0]), int(newCoordinates[1])] = 2
        map[int(oldCoordinates[0]), int(oldCoordinates[1])] = 0
        return True


# Checks if there is an event at the position you are moving to.
def eventCheck(oldCoords, newCoords):
    # If you didn't move for some reason, go back to the last space you were at.
    if not eventAtPosition(newCoords, oldCoords):
        return oldCoords
    # if you did move, return your new coordinates
    else:
        eventAtPosition(newCoords, oldCoords)
        return newCoords


# Move in a direction, returns coordinate of where the character ended up.
def move(coords, direction):
    oldCoords = np.array(coords)
    # If you are going west, go left one column.
    if direction == "west":
        modifier = np.array([0, -1])
        newCoords = oldCoords.__add__(modifier)
        return eventCheck(oldCoords, newCoords)
    # If you are going east, go right one column.
    elif direction == "east":
        modifier = np.array([0, 1])
        newCoords = oldCoords.__add__(modifier)
        return eventCheck(oldCoords, newCoords)
    # If you are going south, go down one row.
    elif direction == "south":
        modifier = np.array([1, 0])
        newCoords = oldCoords.__add__(modifier)
        return eventCheck(oldCoords, newCoords)
    # If you are going north, go up one row.
    elif direction == "north":
        modifier = np.array([-1, 0])
        newCoords = oldCoords.__add__(modifier)
        return eventCheck(oldCoords, newCoords)

#Cool ascii art at the beginning of the game.
banner = pyfiglet.figlet_format("PyQuest")
print(banner)
print("Adventurer! Quickly! We need your help!")
name = input("What is your name? :")

"""Catching null character names to prevent errors later in the game. """
while name is "":
    print("You must have a name! I will ask again...")
    name = input("What is your name, adventurer? :")
print("Terrible times have struck, " + name + " a dark evil lurks within the dungeon!")
print("The world is in peril, quick! Get into the dungeon and defeat the sorcerer. Only then"
      " will this evil be stopped!")
print("The dungeon is down there, please! you must hurry!")
print("You enter down a long, dark staircase. As you are walking down, you notice the floor caving in!")
print("You slide down a massive tunnel until you finally fall into a dark chamber.")
print("The air is musky, and you hear terrible noises lurking deep within the darkness.")

"""This is 'explore mode', where you navigate through the map based on the input you provide to the program. """

while not dead and not isAtEnd:
    command = input("What would you like to do? (Type 'help' for a move set.) :")
    command = command.lower()
    # Moving.
    if "move" in command:
        try:
            movement = command.split(" ")
            # Choosing a direction
            if movement[1] == "south" or movement[1] == 'north' or movement[1] == 'east' or movement[1] == "west":
                coordinates = move(coordinates, movement[1])
            else:
                # Program did not understand your direction "north, south, east, west"
                print("invalid direction: " + "'" + movement[1] + "'")
                print("valid options are: 'north', 'west', 'south', and 'east'.")

        # You typed a move command where the movement list didn't have two indexes.
        except IndexError:
            print("invalid move command.")


    # Command List.
    elif "help" in command:
        showMoveList()
    # show the map.
    elif "map" in command:
        showMap()
    # Inventory.
    elif "inventory" in command:
        print(showInventory(inventory))

    elif "health" in command:
        print("Your health is: " + str(health) + ".")
        #Drink a health potion out of combat
    elif "drink" in command:
        drink(inventory, health)

    # Quit the game
    elif "exit" in command:
        print("Thank you for playing PyQuest!")
        break

    # Did not understand your command.
    else:
        print("Not a command: " + command)

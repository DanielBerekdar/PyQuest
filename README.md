PyQuest  

Version 1.0

I. Introduction

	PyQuest is an interactive text based role playing game based on classic turn based RPG's and Diablo 1 style dungeon crawling!
	PyQuest has the look and feel of classic text based role playing games from the 1970s and 1970s with aspects of more modern games.
	


II. Installation 

	The dependencies are: NumPy, Pandas, and PyFiglet, and having Python 3 installed on your computer.
	
	To download Python, please click the following link, select your operating system, and follow Python's official installation guide: https://www.python.org/downloads/

	You can use pip to install the reqired packages to your computer using the following commands:
	
		pip install numpy
		pip install pandas
		pip install pyfiglet

	Finally, to run the game, you can extract the game files to a directory of your choosing, navigate to that directory with a CD command EX: 'cd /Desktop/', 
	and Enter the following command in your terminal: 
		
		 Python3 pyQuestMain.py 
	By default, the application is in the 'Source Code' directory.


III. How To Play

	There are two states to the game. The main state is "Map Explore" mode where you explore the map and trigger events based on where you walk. 
	The commands set for this mode is as follows:

		move -> 'move [direction]'. This will move you one space in the direction you specify. ex: 'move west'
		
		map -> Displays the map

		drink -> Drinks a health potion (+30 hp)

		inventory -> Views your inventory.

		health -> Shows your health

		exit -> Exit PyQuest.
	
	If you forget these instructions at any point, you can type 'help' to show this move set agian.
	
	The next state is combat where you have the following abilities:
	
		attack -> Attack's an enemy NPC.
	
		defend - > A defensive stance, defends for 90% of the damage but deals a very weak blow.
	
		drink -> Drink a health potion.

	The goal of the game is to kill the evil sorcerer and save the world from his experiments.
	Best of luck, Adventurers!

	
IV. Version Control
	
	This is a project for my CS632 Topics in Python Programming course, however I will make revisions to the game in the future.
	You can view these revisions at the following link:

	


	

	

	



	

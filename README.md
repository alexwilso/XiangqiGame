# Xiangqi Game
This module is an engine for the Xiangqi game made for CS162. Similar to American Chess with a few differences.
The object of the game is to put the enemy's general in a position in which they cannot escape being captured. When no move can be made to prevent the general's capture, checkmate is called and the game is won by the other player. The game consist of two players, red and black. The board consist of rows labeled 1-9 and columns labeled a-i. Moves are completed using make move method that takes string that represents square to move from and square to move to. Ex. make_move("a1", "b2"). To begin instantiate a new XiangqiGame object.

# Installation 
1. Download a version of python 3.7.7 or greater. 
2. Install pygame using pip tool with "python3 -m pip install -U pygame --user"
2. Clone the XiangqiGame repository 
3. Open file using IDE that runs python.

# How to use?
To run XiangqiGame.py initiate XiangqiGame object. Then make movese using the following format.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;game = XiangqiGame()  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;game.make_move('c1', 'e3')  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;game.red_in_check()   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;game.make_move('e7', 'e6')  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;game.get_game_state()  
To run XiangqiGameMain.py make sure pygame is installed on system and run file.

# Built With 
Python 3.7         
Pygame 1.9.6

# Example 
![](XiangqiGame/Images/XiangqiGame.gif)

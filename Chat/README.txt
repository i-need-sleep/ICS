Demo video: https://www.youtube.com/watch?v=DpIi5hA4Nnk edited by Ryan

Notes on using the chat system: 
1.Launch the server first, and then chat_cmdl_client.
2.For textual input, type in the second line (or lower) in the input box. Any input in the first line will not be processed.
3.To properly exit the system, use the exit function in the functions menu. Do not click the exit buttion on the top right.
4.Oversized file transfer (>~1MB?) causes the system to crash.
5.The game requires the pygame module.
6.If you are not running the game on the server machine, dump all the image files into C:/users/[your_user_name].
7.Do not click/type in the main chat window with the game window open.

GUI, file transfer, game integration into the chat system, game learderboard, game autoplay and naming the chat system
(everything except the base game) implemented by Yichen Huang (Will) (yh2689/N11354566).

GUI implemented in chatGUI (mainly), chat_cmdl_client and chat_state_machine
	The manual multi-threading problem is bypassed by bouncing between chat GUI and chat_cmdl_client.
		chat_cmdl_client initiates the mainloop for GUI in chatGUI and as the cursor moves into the chat box, 
		an event triggers the mainloop for the chat system in chat_cmdl_client.
	All inputs in the GUI is processed through modifying cmdl.client.GUI_input.
	The menu function for calling time/who/p/?/c/exiting/file_transfer is implemented through sending a spectific int (so it's not confused with str).
		Some functions (?/p) modifies additional variables that carry the detail of the request.
		Given menu functions (time/who/p/?) now also works when chatting.
		bye command is disabled, use the menu command "quit chat" to quit chat
		Selecting connect in the menu now pops up a window showing all users online.
	The options are pretty much self-explanatory.
		Note that selecting DarkMode/PastaMode when already in that mode togges it off.
		Also, the default directory for file transfer is D:\, which can be changed in the preference menu.
File transfer implemented in chatGUI, chat_state_machine and chat_server
	*It only works with small files (<~100KB) due to problems with JSON decoder (JSONDecodeError: Unterminated string starting at)
	*I'm considering improving it by spliting the file into smaller packs but probably won't be able to finish it in time
	*UPDATE: I did manage to implement that, but still problems occur for larger files (>~1MB) that require more than a dozen of packs
	 	 but anyways, I feel that's good enough for me considering the time I'm allowed.
	The binary data in the chosen file is encoded into a string (read_binary --> b64encode --> utf-8 decode).
	A new action "file" is added, which is similar to text exchange, except it also carries the encoded string and the file name.
	The receving client decodes the string into binary data and writes it into a file with the same file name as the original file.
Game leaderboard implemented in chatGUI, chat_state_machine and chat_server
	Creats a dictionary on the server end that holds leaderboard info
	The dictionary is updated every time a user submits a score
	Returns the dictonaty when the client asks to view the leaderboard
Game Autoplay in bullet_hell_autoplay
	The idea was to implement auto play using machine learning.
	Then I realised I don't have time to do that so I decided to implement a scripted one.
	For demo purposes, gameover is disabled in autoplay. Launch bullet_hell_autoplay_gameoverEnabled for a version with gameover.
	The logic: the priority is not to run into walls
	if the wall is not close sense() gets the info about the closest danger (location, movement vector)
	evade() calculates the normal vector using the movement vector and the locations of the danger and the player
	to figure out which action to take (move up/down/left/right).
	if no danger is close, try to get back to the center
	*I am aware that this algorithm does not always work. For instance, two bullets going parallel towards the player will cause a certain gameover and the player may be conored sometimes.
	Still, the autoplay can survive longer than regular human players (Ryan and I) can ever do in the best cases.
	
Note for the bullet hell game
Implemented by Ryan Yuan zy1223 N13179201

---------For Adults Only----------
----------Introduction------------
------------------------------------
This game aims to let users avoid collision with the various enemies and the bullets, simple and easy!
------------------------------------
------How to play the game------
------------------------------------
 ¡û ¡ü ¡ú ¡ý  ----- movement
P ----- changing backgrounds
M ----- back to the introduction menu
R ----- restart at anytime
ESC ----- quit the game at anytime
------------------------------------
----------Game mode-------------
------------------------------------
There are three modes to choose everytime you play, including touhou project(¶«·½project), philosophy memes(¡á) and gundam(¸Õ´óÄ¾)
After choosing mode there are three stages to choose difficulties including the amount of bullets and enemies respectively and the time you need to survive
For each, there are five available difficulties, easy, normal, hard, very hard and extreme(not for human), think carefully before you choose XD
Then, you are ready to challenge!
------------------------------------
---------About Death-------------
------------------------------------
What will trigger death?
collision with wall, bullets or enemies, so it is easy to die, be careful!
The death note will be in three types referring to recent famous memes, don't be angry when you die XD
------------------------------------
-------About this game-----------
------------------------------------
I import pygame as the basic library from python to write this game, 
using its internal functions 
pygame.display.set_mode( ) ------ setting the size of the game window,
pygame.image.load( ) ----- importing images from outside,
pygame.font.Font( ) ----- setting the fonts of the output letters
pygame.mouse.get_pressed( ) ------ get the status of the mouse click
pygame.draw.rect( ) ------ drawing rectangle blocks
pygame.event.get( ) ------ getting the condition of the keyboard
For the rest I use basic concepts like for loop to write the game, combined with random functions as the enemies are randomly generated
I use several lists for each objects to store their status including their position and their speed, each has its own index and will be automatically deleted after flying out the borderline



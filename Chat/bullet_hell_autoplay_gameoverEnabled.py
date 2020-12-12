# -*- coding: utf-8 -*-
"""
Created on Mon May  6 13:31:48 2019

@author: 86189
"""

import pygame
import random
import time
from math import sqrt
    



#----------------------------------
#game features and color settings
display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)

gray = (55,55,55)
pink = (200,50,100)

red = (255,100,0)
green = (100,200,0)
blue = (100,150,255)

brightblue = (100,100,255)

darkred = (200,0,0)
darkgreen = (0,200,0)
darkblue = (100,100,200)

yellow = (255,255,150)


background_color1 = (255,255,255)
background_color2 = (0,0,255)
touhouImg_list = ['012_WPS图片.png','F.png','20140509235309_2WzLr_WPS图片.png','135234885_WPS图片.png','0ff41bd5ad6eddc4633c23ea3adbb6fd536633c3_WPS图片.png']
gundamImg_list = ['dahe_WPS图片.png','xiaya_WPS图片.png','feiniao_WPS图片.png','keluze_WPS图片.png','images_WPS图片_WPS图片.png']
zhexueImg_list = ['van_WPS图片.png','bili.png','chijiang_WPS图片.png','xiangjiao_WPS图片.png','yeshou_WPS图片.png']
    
#----------------------------------
#setting up the title and importing the images
def start():
    pygame.init()
    global imagehi
    global gameDisplay
    global clock
    global display_Img
    global player_Img
    savefile_opened_or_created = list()
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('bullet hell')
    clock = pygame.time.Clock()
    image_list  = ['parallel-800.jpg', 'wallpapersden.com_outrun-pixel-sunset_800x600_WPS图片.jpg', 'wallpapersden.com_synthwave-8-bit-pixel-cityscape_800x600.jpg', 'throne_room_dribbble.png']
    imagehi=[]
    for i in image_list:
        imagehi.append( pygame.image.load(i))
    display_Img = pygame.image.load(random.choice(image_list))
    
    game_intro()
#----------------------------------
#setting up the font color functions
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def text_objects_blue(text, font):
    textSurface = font.render(text, True, blue)
    return textSurface, textSurface.get_rect()
    
def text_objects_darkred(text, font):
    textSurface = font.render(text, True, darkred)
    return textSurface, textSurface.get_rect()

def text_objects_darkgreen(text, font):
    textSurface = font.render(text, True, darkgreen)
    return textSurface, textSurface.get_rect()
#------------------------------------
#game introductioin part
def game_intro():
    global imagehi
    global gameDisplay
    choose_status = False
   
    left_clicked = True
    
    index=0
    while choose_status:
        
        for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
           if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:   
               pygame.quit()
           if event.type == pygame.KEYDOWN and event.key == pygame.K_p: 
               index+=1
               if index == 4:
                   index = 0
        display_Img = imagehi[index]    
        gameDisplay.blit(display_Img,(0,0)) 
        largeText = pygame.font.Font('freesansbold.ttf', 50)
        TextSurf, TextRect = text_objects_darkred('BULLET HELL', largeText)
        TextRect.center = ((display_width/2), (100))
        gameDisplay.blit(TextSurf, TextRect)
        
        mouse_pos = pygame.mouse.get_pos()
        x_mouse = mouse_pos[0]
        y_mouse = mouse_pos[1]
        
        mouse_pressed = pygame.mouse.get_pressed()
                
        if x_mouse > 325 and x_mouse < 475 and y_mouse > 500 and y_mouse < 550:
            pygame.draw.rect(gameDisplay, blue, (325, 500, 150, 50))
            if mouse_pressed[0] == 1 and left_clicked == False:
                choose_status = False
        else:
             pygame.draw.rect(gameDisplay, darkblue, (325, 500, 150, 50))
        
             
        if left_clicked == False and mouse_pressed[0] == 1:
            left_clicked = True
        elif left_clicked == True and mouse_pressed[0] == 0:
            left_clicked = False
        
        h = 0
        introduction_list = ['Move Left ----- Left Arrow', 'Move Right ----- Right Arrow', 'Move Up ----- Up Arrow', 'Move Down ----- Down Arrow', 'Restart Game ----- R', 'Exit ----- Esacpe', 'Change background ----- P', 'Back to menu ----- M', 'Other functions under construction', 'Press the button to start playing!']
        
        for i in introduction_list:
            smallText = pygame.font.Font('C:\Windows\Fonts\Verdana.ttf', 20)
            TextSurf, TextRect = text_objects_darkgreen(i, smallText)
            TextRect.center = ((400), (170 + h))
            gameDisplay.blit(TextSurf, TextRect)
            h += 30
        
        smallText = pygame.font.Font('C:\Windows\Fonts\simkai.ttf', 20)
        TextSurf, TextRect = text_objects('开始游戏', smallText)
        TextRect.center = ((400), (525))
        gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(60)

    game_loop()   
#---------------------------------------------    
#setting up the main game loop
def game_loop():
    global display_Img
    global walk_left
    global walk_right
    global walk_up
    global walk_down
    global x_player
    global y_player
    global position
    global speed
    death_note = [['菜', '你玩游戏像菜虚鲲'], ['死', '犹豫，就会败北'], ['死', '果断，就会白给']]
    death = random.choice(death_note)

    choose_difficulty = False
    
    left_clicked = True
    
    index = 0
    
    choose_mode = False
    
    mode_one = False
    
    mode_two = False
    
    mode_three = True
#before starting the game, to set up the game mode and the difficulties    
#    while choose_mode:
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                pygame.quit()
#            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:   
#                pygame.quit()
#            if event.type == pygame.KEYDOWN and event.key == pygame.K_p: 
#               index += 1
#               if index == 4:
#                   index = 0
#            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
#                game_intro()
#                   
#        display_Img = imagehi[index]                 
#        gameDisplay.blit(display_Img,(0,0))
#        
#        largeText = pygame.font.Font('freesansbold.ttf', 50)
#        TextSurf, TextRect = text_objects_darkred('Choose your mode', largeText)
#        TextRect.center = ((display_width/2),(display_height/2))
#        gameDisplay.blit(TextSurf, TextRect)
#        
#        mouse_pos = pygame.mouse.get_pos()
#        x_mouse = mouse_pos[0]
#        y_mouse = mouse_pos[1]
#        
#        mouse_pressed = pygame.mouse.get_pressed()
#                
#        if x_mouse > 150 and x_mouse < 300 and y_mouse > 500 and y_mouse < 550:
#            pygame.draw.rect(gameDisplay, blue, (150, 500, 150, 50))
#            if mouse_pressed[0] == 1 and left_clicked == False:
#                choose_mode = False
#                mode_one = True
#        else:
#             pygame.draw.rect(gameDisplay, darkblue, (150, 500, 150, 50))
#             
#        if x_mouse > 325 and x_mouse < 475 and y_mouse > 500 and y_mouse < 550:
#            pygame.draw.rect(gameDisplay, blue, (325, 500, 150, 50))
#            if mouse_pressed[0] == 1 and left_clicked == False:
#                choose_mode = False
#                mode_two = True
#        else:
#             pygame.draw.rect(gameDisplay, darkblue, (325, 500, 150, 50))
#        
#        if x_mouse > 500 and x_mouse < 650 and y_mouse > 500 and y_mouse < 550:
#            pygame.draw.rect(gameDisplay, blue, (500, 500, 150, 50))
#            if mouse_pressed[0] == 1 and left_clicked == False:
#                choose_mode = False
#                mode_three = True
#        else:
#             pygame.draw.rect(gameDisplay, darkblue, (500, 500, 150, 50))
#             
#        if left_clicked == False and mouse_pressed[0] == 1:
#            left_clicked = True
#        elif left_clicked == True and mouse_pressed[0] == 0:
#            left_clicked = False
#            
#        smallText = pygame.font.Font('C:\Windows\Fonts\simkai.ttf', 20)
#        TextSurf, TextRect = text_objects('东方Project', smallText)
#        TextRect.center = ((225), (525))
#        gameDisplay.blit(TextSurf, TextRect)
#        
#        smallText = pygame.font.Font('C:\Windows\Fonts\simkai.ttf', 20)
#        TextSurf, TextRect = text_objects('新日暮里♂', smallText)
#        TextRect.center = ((400), (525))
#        gameDisplay.blit(TextSurf, TextRect)
#
#        
#        smallText = pygame.font.Font('C:\Windows\Fonts\simkai.ttf', 20)
#        TextSurf, TextRect = text_objects('不要停下来啊', smallText)
#        TextRect.center = ((575), (525))
#        gameDisplay.blit(TextSurf, TextRect)
#        pygame.display.update()
#        clock.tick(60)
        
    if mode_one == True:
        player_Img = pygame.image.load(touhouImg_list[4])
    if mode_two == True:
        player_Img = pygame.image.load(zhexueImg_list[4])
    if mode_three == True:
        player_Img = pygame.image.load(gundamImg_list[4])
    
#    while choose_difficulty:
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                pygame.quit()
#            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:   
#                pygame.quit()
#            if event.type == pygame.KEYDOWN and event.key == pygame.K_p: 
#               index += 1
#               if index == 4:
#                   index = 0
#            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
#                game_intro()
#                   
#        display_Img = imagehi[index]                 
#        gameDisplay.blit(display_Img,(0,0))
#        
#        largeText = pygame.font.Font('freesansbold.ttf', 50)
#        TextSurf, TextRect = text_objects_darkred('Amount of bullets difficulty', largeText)
#        TextRect.center = ((display_width/2),(display_height/2))
#        gameDisplay.blit(TextSurf, TextRect)
#        
#        mouse_pos = pygame.mouse.get_pos()
#        x_mouse = mouse_pos[0]
#        y_mouse = mouse_pos[1]
#        
#        mouse_pressed = pygame.mouse.get_pressed()
#        
#        if x_mouse > 150 and x_mouse < 250 and y_mouse > 175 and y_mouse < 225:
#            pygame.draw.rect(gameDisplay, green, (150, 175, 100, 50))
#            if mouse_pressed[0] == 1 and left_clicked == False:
#                difficulty = 'easy'
#                choose_difficulty = False
#        else:
#            pygame.draw.rect(gameDisplay, darkgreen, (150, 175, 100, 50))
#        
#        if x_mouse > 350 and x_mouse < 450 and y_mouse > 175 and y_mouse < 225:
#            pygame.draw.rect(gameDisplay, green, (350, 175, 100, 50))
#            if mouse_pressed[0] == 1 and left_clicked == False:
#                difficulty = 'normal'
#                choose_difficulty = False
#        else:
#            pygame.draw.rect(gameDisplay, darkgreen, (350, 175, 100, 50))
#        
#        if x_mouse > 550 and x_mouse < 650 and y_mouse > 175 and y_mouse < 225:
#            pygame.draw.rect(gameDisplay, green, (550, 175, 100, 50))
#            if mouse_pressed[0] == 1 and left_clicked == False:
#                difficulty = 'hard'
#                choose_difficulty = False
#        else:
#            pygame.draw.rect(gameDisplay, darkgreen, (550, 175, 100, 50))
#            
#        if x_mouse > 250 and x_mouse < 350 and y_mouse > 375 and y_mouse < 425:
#            pygame.draw.rect(gameDisplay, green, (250, 375, 100, 50))
#            if mouse_pressed[0] == 1 and left_clicked == False:
#                difficulty = 'very hard'
#                choose_difficulty = False
#        else:
#            pygame.draw.rect(gameDisplay, darkgreen, (250, 375, 100, 50))    
#        
#        if x_mouse > 450 and x_mouse < 550 and y_mouse > 375 and y_mouse < 425:
#            pygame.draw.rect(gameDisplay, green, (450, 375, 100, 50))
#            if mouse_pressed[0] == 1 and left_clicked == False:
#                difficulty = 'extreme'
#                choose_difficulty = False
#        else:
#            pygame.draw.rect(gameDisplay, darkgreen, (450, 375, 100, 50)) 
#            
#        if left_clicked == False and mouse_pressed[0] == 1:
#            left_clicked = True
#        elif left_clicked == True and mouse_pressed[0] == 0:
#            left_clicked = False
#            
#        smallText = pygame.font.Font('freesansbold.ttf', 20)
#        TextSurf, TextRect = text_objects('EASY', smallText)
#        TextRect.center = ((200), (200))
#        gameDisplay.blit(TextSurf, TextRect)
#        
#        smallText = pygame.font.Font('freesansbold.ttf', 20)
#        TextSurf, TextRect = text_objects('NORMAL', smallText)
#        TextRect.center = ((400), (200))
#        gameDisplay.blit(TextSurf, TextRect)
#        
#        smallText = pygame.font.Font('freesansbold.ttf', 20)
#        TextSurf, TextRect = text_objects('HARD', smallText)
#        TextRect.center = ((600), (200))
#        gameDisplay.blit(TextSurf, TextRect)
#        
#        smallText = pygame.font.Font('freesansbold.ttf', 15)
#        TextSurf, TextRect = text_objects('VERY HARD', smallText)
#        TextRect.center = ((300), (400))
#        gameDisplay.blit(TextSurf, TextRect)
#        
#        smallText = pygame.font.Font('freesansbold.ttf', 20)
#        TextSurf, TextRect = text_objects('EXTREME', smallText)
#        TextRect.center = ((500), (400))
#        gameDisplay.blit(TextSurf, TextRect)
#        
#        pygame.display.update()
#        clock.tick(60)
    
    difficulty = 'extreme'    
    choose_difficulty = False
    
    left_clicked = True
    
#    while choose_difficulty:
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                pygame.quit()
#            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:   
#                pygame.quit()
#            if event.type == pygame.KEYDOWN and event.key == pygame.K_p: 
#               index += 1
#               if index == 4:
#                   index = 0
#            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
#                game_intro()
#                   
#        display_Img = imagehi[index]                
#        gameDisplay.blit(display_Img,(0,0))
#        
#        largeText = pygame.font.Font('freesansbold.ttf', 50)
#        TextSurf, TextRect = text_objects_darkred('Amount of enemies difficulty', largeText)
#        TextRect.center = ((display_width/2),(display_height/2))
#        gameDisplay.blit(TextSurf, TextRect)
#        
#        mouse_pos = pygame.mouse.get_pos()
#        x_mouse = mouse_pos[0]
#        y_mouse = mouse_pos[1]
#        
#        mouse_pressed = pygame.mouse.get_pressed()
#        
#        if x_mouse > 150 and x_mouse < 250 and y_mouse > 175 and y_mouse < 225:
#            pygame.draw.rect(gameDisplay, green, (150, 175, 100, 50))
#            if mouse_pressed[0] == 1 and left_clicked == False:
#                enemies_difficulty = 'easy'
#                choose_difficulty = False
#        else:
#            pygame.draw.rect(gameDisplay, darkgreen, (150, 175, 100, 50))
#        
#        if x_mouse > 350 and x_mouse < 450 and y_mouse > 175 and y_mouse < 225:
#            pygame.draw.rect(gameDisplay, green, (350, 175, 100, 50))
#            if mouse_pressed[0] == 1 and left_clicked == False:
#                enemies_difficulty = 'normal'
#                choose_difficulty = False
#        else:
#            pygame.draw.rect(gameDisplay, darkgreen, (350, 175, 100, 50))
#        
#        if x_mouse > 550 and x_mouse < 650 and y_mouse > 175 and y_mouse < 225:
#            pygame.draw.rect(gameDisplay, green, (550, 175, 100, 50))
#            if mouse_pressed[0] == 1 and left_clicked == False:
#                enemies_difficulty = 'hard'
#                choose_difficulty = False
#        else:
#            pygame.draw.rect(gameDisplay, darkgreen, (550, 175, 100, 50))
#            
#        if x_mouse > 250 and x_mouse < 350 and y_mouse > 375 and y_mouse < 425:
#            pygame.draw.rect(gameDisplay, green, (250, 375, 100, 50))
#            if mouse_pressed[0] == 1 and left_clicked == False:
#                enemies_difficulty = 'very hard'
#                choose_difficulty = False
#        else:
#            pygame.draw.rect(gameDisplay, darkgreen, (250, 375, 100, 50))    
#        
#        if x_mouse > 450 and x_mouse < 550 and y_mouse > 375 and y_mouse < 425:
#            pygame.draw.rect(gameDisplay, green, (450, 375, 100, 50))
#            if mouse_pressed[0] == 1 and left_clicked == False:
#                enemies_difficulty = 'extreme'
#                choose_difficulty = False
#        else:
#            pygame.draw.rect(gameDisplay, darkgreen, (450, 375, 100, 50)) 
#            
#        if left_clicked == False and mouse_pressed[0] == 1:
#            left_clicked = True
#        elif left_clicked == True and mouse_pressed[0] == 0:
#            left_clicked = False
#            
#        smallText = pygame.font.Font('freesansbold.ttf', 20)
#        TextSurf, TextRect = text_objects('EASY', smallText)
#        TextRect.center = ((200), (200))
#        gameDisplay.blit(TextSurf, TextRect)
#        
#        smallText = pygame.font.Font('freesansbold.ttf', 20)
#        TextSurf, TextRect = text_objects('NORMAL', smallText)
#        TextRect.center = ((400), (200))
#        gameDisplay.blit(TextSurf, TextRect)
#        
#        smallText = pygame.font.Font('freesansbold.ttf', 20)
#        TextSurf, TextRect = text_objects('HARD', smallText)
#        TextRect.center = ((600), (200))
#        gameDisplay.blit(TextSurf, TextRect)
#        
#        smallText = pygame.font.Font('freesansbold.ttf', 15)
#        TextSurf, TextRect = text_objects('VERY HARD', smallText)
#        TextRect.center = ((300), (400))
#        gameDisplay.blit(TextSurf, TextRect)
#        
#        smallText = pygame.font.Font('freesansbold.ttf', 20)
#        TextSurf, TextRect = text_objects('EXTREME', smallText)
#        TextRect.center = ((500), (400))
#        gameDisplay.blit(TextSurf, TextRect)
#        
#        pygame.display.update()
#        clock.tick(60)
        
    enemies_difficulty = 'extreme'
    choose_difficulty = False
    
    left_clicked = True
    
#    while choose_difficulty:
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                pygame.quit()
#            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:   
#                pygame.quit()
#            if event.type == pygame.KEYDOWN and event.key == pygame.K_p: 
#               index += 1
#               if index == 4:
#                   index = 0
#            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
#                game_intro()
#                   
#        display_Img = imagehi[index]                
#        gameDisplay.blit(display_Img,(0,0))
#        
#        largeText = pygame.font.Font('freesansbold.ttf', 40)
#        TextSurf, TextRect = text_objects_darkred('Survival Time', largeText)
#        TextRect.center = ((display_width/2),(display_height/2))
#        gameDisplay.blit(TextSurf, TextRect)
#        
#        mouse_pos = pygame.mouse.get_pos()
#        x_mouse = mouse_pos[0]
#        y_mouse = mouse_pos[1]
#        
#        mouse_pressed = pygame.mouse.get_pressed()
#        
#        if x_mouse > 150 and x_mouse < 250 and y_mouse > 175 and y_mouse < 225:
#            pygame.draw.rect(gameDisplay, green, (150, 175, 100, 50))
#            if mouse_pressed[0] == 1 and left_clicked == False:
#                time_difficulty = 'easy'
#                choose_difficulty = False
#        else:
#            pygame.draw.rect(gameDisplay, darkgreen, (150, 175, 100, 50))
#        
#        if x_mouse > 350 and x_mouse < 450 and y_mouse > 175 and y_mouse < 225:
#            pygame.draw.rect(gameDisplay, green, (350, 175, 100, 50))
#            if mouse_pressed[0] == 1 and left_clicked == False:
#                time_difficulty = 'normal'
#                choose_difficulty = False
#        else:
#            pygame.draw.rect(gameDisplay, darkgreen, (350, 175, 100, 50))
#        
#        if x_mouse > 550 and x_mouse < 650 and y_mouse > 175 and y_mouse < 225:
#            pygame.draw.rect(gameDisplay, green, (550, 175, 100, 50))
#            if mouse_pressed[0] == 1 and left_clicked == False:
#                time_difficulty = 'hard'
#                choose_difficulty = False
#        else:
#            pygame.draw.rect(gameDisplay, darkgreen, (550, 175, 100, 50))
#            
#        if x_mouse > 250 and x_mouse < 350 and y_mouse > 375 and y_mouse < 425:
#            pygame.draw.rect(gameDisplay, green, (250, 375, 100, 50))
#            if mouse_pressed[0] == 1 and left_clicked == False:
#                time_difficulty = 'very hard'
#                choose_difficulty = False
#        else:
#            pygame.draw.rect(gameDisplay, darkgreen, (250, 375, 100, 50))    
#        
#        if x_mouse > 450 and x_mouse < 550 and y_mouse > 375 and y_mouse < 425:
#            pygame.draw.rect(gameDisplay, green, (450, 375, 100, 50))
#            if mouse_pressed[0] == 1 and left_clicked == False:
#                time_difficulty = 'extreme'
#                choose_difficulty = False
#        else:
#            pygame.draw.rect(gameDisplay, darkgreen, (450, 375, 100, 50)) 
#            
#        if left_clicked == False and mouse_pressed[0] == 1:
#            left_clicked = True
#        elif left_clicked == True and mouse_pressed[0] == 0:
#            left_clicked = False
#            
#        smallText = pygame.font.Font('freesansbold.ttf', 20)
#        TextSurf, TextRect = text_objects('EASY', smallText)
#        TextRect.center = ((200), (200))
#        gameDisplay.blit(TextSurf, TextRect)
#        
#        smallText = pygame.font.Font('freesansbold.ttf', 20)
#        TextSurf, TextRect = text_objects('NORMAL', smallText)
#        TextRect.center = ((400), (200))
#        gameDisplay.blit(TextSurf, TextRect)
#        
#        smallText = pygame.font.Font('freesansbold.ttf', 20)
#        TextSurf, TextRect = text_objects('HARD', smallText)
#        TextRect.center = ((600), (200))
#        gameDisplay.blit(TextSurf, TextRect)
#        
#        smallText = pygame.font.Font('freesansbold.ttf', 15)
#        TextSurf, TextRect = text_objects('VERY HARD', smallText)
#        TextRect.center = ((300), (400))
#        gameDisplay.blit(TextSurf, TextRect)
#        
#        smallText = pygame.font.Font('freesansbold.ttf', 20)
#        TextSurf, TextRect = text_objects('EXTREME', smallText)
#        TextRect.center = ((500), (400))
#        gameDisplay.blit(TextSurf, TextRect)
#        
#        pygame.display.update()
#        clock.tick(60)
    time_difficulty = 'extreme'
#-----------------------------------
#necessary presets of the game including the player status and the eenemies status         
    x_player = 400
    y_player = 300
    
    gameExit = False
    
    screen = 1
    
    walk_left = False
    walk_right = False
    walk_up = False
    walk_down = False
    slow_down = False
    
    game_over = False
    
    restart = False
    
    time1 = 0
    score = 0
    x_bullet = list()
    y_bullet = list()
    x_bullet_speed = list()
    y_bullet_speed = list()
    bullet_color = list()
    
    x_bullet_type_2 = list()
    y_bullet_type_2 = list()
    x_bullet_type_2_speed = list()
    y_bullet_type_2_speed = list()
    bullet_type_2_color = list()
    
    x_bullet_type_3 = list()
    y_bullet_type_3 = list()
    x_bullet_type_3_speed = list()
    y_bullet_type_3_speed = list()
    bullet_type_3_color = list()
    
    x_yellow_enemie = list()
    y_yellow_enemie = list()
    yellow_enemie_speed_x = -3
    
    x_green_enemie = list()
    y_green_enemie = list()
    green_enemie_speed_y = -2
    
    x_red_enemie = list()
    y_red_enemie = list()
    red_enemie_speed_y = 5
    
    x_blue_enemie = list()
    y_blue_enemie = list()
    blue_enemie_speed_x = 2.5
    
    
       
    yellow_time = 90
    green_time = 0
    red_time = 0
    blue_time = 0
    
    bullet_time = 0
    end_score = []
    time_survive = 0
    
    interval = 0.01
    latest = 0.0
#game skeleton    
    while not gameExit:
#trigger        
        
        
        for event in pygame.event.get():
            
#            if event.type == 2 and event.key == 276:
#                walk_left = True
#                
#            if event.type == 3 and event.key == 276:
#                walk_left = False
#                
#            if event.type == 2 and event.key == 275:
#                walk_right = True
#                
#            if event.type == 3 and event.key == 275:
#                walk_right = False
#            
#            if event.type == 2 and event.key == 274:
#                walk_down = True
#                
#            if event.type == 3 and event.key == 274:
#                walk_down = False
#                
#            if event.type == 2 and event.key == 273:
#                walk_up = True
#                
#            if event.type == 3 and event.key == 273:
#                walk_up = False
#                
#            if event.type == 2 and event.key == pygame.K_r:
#                restart = True
#            
#            if event.type == 3 and event.key == pygame.K_r:
#                restart = False
#            
#            if event.type == 2 and event.key == pygame.K_LSHIFT:
#                slow_down == True
#            
#            if event.type == 3 and event.key == pygame.K_LSHIFT:
#                slow_down == False
#                
                
            mouse_pressed = pygame.mouse.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:   
                pygame.quit()
                
        gameDisplay.blit(display_Img,(0,0))
        
        mouse_pressed = pygame.mouse.get_pressed()
        
        if mouse_pressed[2] == 1:
            gameExit = True
            game_intro()
#setting the walls        
        if gameExit == False:
            pygame.draw.rect(gameDisplay, gray, (0, 0, 30, 600))
            pygame.draw.rect(gameDisplay, gray, (0, 0, 800, 30))
            pygame.draw.rect(gameDisplay, gray, (770, 0, 30, 600))
            pygame.draw.rect(gameDisplay, gray, (770, 0, 30, 600))
            pygame.draw.rect(gameDisplay, gray, (0, 570, 800, 30))
#setting the game over condtions            
            if x_player > 765:
                game_over = True   
            if x_player < 35:
                game_over = True
            if y_player > 565:
                game_over = True
            if y_player < 35:
                game_over = True
#setting up the difficulty features including how fast the enemies generate and how many scores can the player get                
            if time_difficulty == 'easy':
                time1 += 5    
                score += 10
            if time_difficulty == 'normal':
                time1 += 3
                score += 20
            if time_difficulty == 'hard':
                time1 += 2
                score += 30
            if time_difficulty == 'very hard':
                time1 += 1.5
                score += 40
            if time_difficulty == 'extreme':
                time1 += 1
                score += 50
                
            if enemies_difficulty == 'easy':
                yellow_time += 0.15
                green_time += 0.15
                red_time += 0.15
                blue_time += 0.15
            if enemies_difficulty == 'normal':
                yellow_time += 0.3
                green_time += 0.3
                red_time += 0.3
                blue_time += 0.3
            if enemies_difficulty == 'hard':
                yellow_time += 0.5
                green_time += 0.5
                red_time += 0.5
                blue_time += 0.5
            if enemies_difficulty == 'very hard':
                yellow_time += 0.75
                green_time += 0.75
                red_time += 0.75
                blue_time += 0.75
            if enemies_difficulty == 'extreme':
                yellow_time += 1
                green_time += 1
                red_time += 1
                blue_time += 1
                
            bullet_time += 1
            
            if difficulty == 'easy' and bullet_time > 199:
                bullet_time = 0
            if difficulty == 'noraml' and bullet_time > 109:
                bullet_time = 0
            if difficulty == 'hard' and bullet_time > 79:
                bullet_time = 0
            if difficulty == 'very hard' and bullet_time > 44:
                bullet_time = 0
            if difficulty == 'extreme' and bullet_time > 19:
                bullet_time = 0
#enemies generating parts based on the time passed               
            if yellow_time > 89 and time1 < 4000:
                yellow_time = 0
                x_yellow_enemie.append(850)
                y_yellow_enemie.append(random.randrange(51,551))
                
            if green_time > 134 and time1 > 800 and time1 < 4000:
                 green_time = 0
                 x_green_enemie.append(random.randrange(51,751))
                 y_green_enemie.append(650)
                 
            if red_time > 59 and time1 < 4000 and time1 > 1600:
                red_time = 0
                x_red_enemie.append(random.randrange(51,751))
                y_red_enemie.append(-50)
                
            if blue_time > 99 and time1 < 4000 and time1 > 2400:
                blue_time = 0
                x_blue_enemie.append(-50)
                y_blue_enemie.append(random.randrange(51,551))
                
            if game_over == False and len(x_bullet) < 1 and len(x_yellow_enemie) < 1 and len(x_blue_enemie) < 1:
                game_loop()
                largeText = pygame.font.Font('C:\Windows\Fonts\simkai.ttf', 70)
                TextSurf, TextRect = text_objects_darkgreen("不妨试试更难的？", largeText)
                TextRect.center = ((display_width/2), (display_height/2))
                gameDisplay.blit(TextSurf, TextRect)
#generating three types of bullets              
            for i in range(len(x_bullet)-1, -1, -1):
                x_bullet[i] += x_bullet_speed[i] * 5
                y_bullet[i] += y_bullet_speed[i] * 5
                
#                if mode_one = True:
#                
#                if mode_two = True:
#                    
#                if mode_three = True:
#                    
                pygame.draw.rect(gameDisplay, bullet_color[i], (x_bullet[i] - 5, y_bullet[i] - 5, 10, 10))
                
                if x_player > x_bullet[i] - 10 and x_player < x_bullet[i] + 10 and y_player > y_bullet[i] - 10 and y_player < y_bullet[i] + 10:
                    game_over = True
                    
                if x_bullet[i] < -25 or x_bullet[i] > 825 or y_bullet[i] > 625 or y_bullet[i] < -25:
                    del x_bullet[i]
                    del y_bullet[i]
                    del x_bullet_speed[i]
                    del y_bullet_speed[i]
                    del bullet_color[i]
                    
            for i in range(len(x_bullet_type_2) - 1, -1, -1):
                x_bullet_type_2[i] += x_bullet_type_2_speed[i] / 5
                y_bullet_type_2[i] += y_bullet_type_2_speed[i] / 2.5
                y_bullet_type_2_speed[i] += 0.4
                
#                if mode_one = True:
#                
#                if mode_two = True:
#                    
#                if mode_three = True:
#                
                pygame.draw.rect(gameDisplay, red, (x_bullet_type_2[i] - 5, y_bullet_type_2[i] - 5, 10, 10))
                
                if x_player > x_bullet_type_2[i] - 10 and x_player < x_bullet_type_2[i] + 10 and y_player > y_bullet_type_2[i] - 10 and y_player < y_bullet_type_2[i] + 10:
                    game_over = True

                if x_bullet_type_2[i] < -25 or x_bullet_type_2[i] > 825 or y_bullet_type_2[i] > 625:
                    del x_bullet_type_2[i]
                    del y_bullet_type_2[i]
                    del x_bullet_type_2_speed[i]
                    del y_bullet_type_2_speed[i]
                    del bullet_type_2_color[i]
                    
            for i in range(len(x_bullet_type_3) - 1, -1, -1):
                x_bullet_type_3[i] += x_bullet_type_3_speed[i] * 5
                y_bullet_type_3[i] += y_bullet_type_3_speed[i] * 5
                
#                if mode_one = True:
#                
#                if mode_two = True:
#                    
#                if mode_three = True:
#                
                pygame.draw.rect(gameDisplay, darkblue, (x_bullet_type_3[i] - 5, y_bullet_type_3[i] - 5, 10, 10))
                
#                if x_player > x_bullet_type_3[i] - 10 and x_player < x_bullet_type_3[i] + 10 and y_player > y_bullet_type_3[i] - 10 and y_player < y_bullet_type_3[i] + 10:
#                    game_over = True

                if x_bullet_type_3[i] < -25 or x_bullet_type_3[i] > 825 or y_bullet_type_3[i] > 625 or y_bullet_type_3[i] < -25:
                    del x_bullet_type_3[i]
                    del y_bullet_type_3[i]
                    del x_bullet_type_3_speed[i]
                    del y_bullet_type_3_speed[i]
                    del bullet_type_3_color[i]
#generating four types of enemies                    
            for i in range(len(x_yellow_enemie) - 1, -1, -1):
                x_yellow_enemie[i] += -3
                
                if mode_one == True:
                    gameDisplay.blit(pygame.image.load(touhouImg_list[0]), (x_yellow_enemie[i] - 15, y_yellow_enemie[i] - 15))
                if mode_two == True:
                    gameDisplay.blit(pygame.image.load(zhexueImg_list[0]), (x_yellow_enemie[i] - 15, y_yellow_enemie[i] - 15))
                if mode_three == True:
                    gameDisplay.blit(pygame.image.load(gundamImg_list[0]), (x_yellow_enemie[i] - 15, y_yellow_enemie[i] - 15))

                if difficulty == 'easy':
                    number = 66                    
                if difficulty == 'normal':
                    number = 46                    
                if difficulty == 'hard':
                    number = 31
                if difficulty == 'very hard':
                    number = 21
                if difficulty =='extreme':
                    number = 11
                    
                if random.randrange(1, number) == 1:
                    x = x_yellow_enemie[i]
                    y = y_yellow_enemie[i]
                    
                    if random.randrange(0, 2) == 1:
                        if random.randrange(0, 2) == 1:
                            x_random = 800
                            y_random = random.randrange(1, 601)
                        else:
                            x_random = 0
                            y_random = random.randrange(1, 601)
                    else:
                        if random.randrange(0,2) == 1:
                            x_random = random.randrange(1,801)
                            y_random = 600
                        else:
                            x_random = random.randrange(1,801)
                            y_random = 0
                    
                    distance = sqrt((x_random - x)**2 + (y_random - y) ** 2)
                    
                    x_speed = (x_random - x) / 240
                    y_speed = (y_random - y) / 240
                    
                    x_speed /= distance / 150
                    y_speed /= distance / 150
                    
                    x_bullet_speed.append(x_speed)
                    y_bullet_speed.append(y_speed)
                    
                    x_bullet.append(x)
                    y_bullet.append(y)
                    
                    bullet_color.append(blue)
                    
#                if x_player > x_yellow_enemie[i] - 15 and x_player < x_yellow_enemie[i] + 15 and y_player > y_yellow_enemie[i] - 15 and y_player < y_yellow_enemie[i] + 15:
#                    game_over = True
                    
                if x_yellow_enemie[i] < -25:
                    del x_yellow_enemie[i]
                    del y_yellow_enemie[i]
                    
#            for i in range(len(x_green_enemie) - 1, -1, -1):
#                y_green_enemie[i] += -2
#                
#                if mode_one == True:
#                    gameDisplay.blit(pygame.image.load(touhouImg_list[1]), (x_green_enemie[i] - 11, y_green_enemie[i] - 15))
#                if mode_two == True:
#                    gameDisplay.blit(pygame.image.load(zhexueImg_list[1]), (x_green_enemie[i] - 11, y_green_enemie[i] - 15))
#                if mode_three == True:
#                    gameDisplay.blit(pygame.image.load(gundamImg_list[1]), (x_green_enemie[i] - 11, y_green_enemie[i] - 15))
##                
#                if difficulty == 'easy':
#                    number = 56                    
#                if difficulty == 'normal':
#                    number = 36                    
#                if difficulty == 'hard':
#                    number = 21
#                if difficulty == 'very hard':
#                    number = 11
#                if difficulty =='extreme':
#                    number = 4
#                    
#                if random.randrange(1, number) == 1:
#                    x = x_green_enemie[i]
#                    y = y_green_enemie[i]
#                    
#                    x_bullet_type_2_speed.append(random.randrange(-30,31))
#                    y_bullet_type_2_speed.append(random.randrange(-20,0))
#                    
#                    x_bullet_type_2.append(x)
#                    y_bullet_type_2.append(y)
#                    
#                    bullet_type_2_color.append(darkred)
#                    
#                if x_player > x_green_enemie[i] - 11 and x_player < x_green_enemie[i] + 12 and y_player > y_green_enemie[i] - 15 and y_player < y_green_enemie[i] + 15:
#                    game_over = True
#                    
#                if y_green_enemie[i] < -25:
#                    del x_green_enemie[i]
#                    del y_green_enemie[i]
#                    
#            for i in range(len(x_red_enemie) - 1, -1, -1):
#                y_red_enemie[i] += 5
#                
#                if mode_one == True:
#                    gameDisplay.blit(pygame.image.load(touhouImg_list[2]), (x_red_enemie[i] - 25, y_red_enemie[i] - 25))
#                if mode_two == True:
#                    gameDisplay.blit(pygame.image.load(zhexueImg_list[2]), (x_red_enemie[i] - 25, y_red_enemie[i] - 25))
#                if mode_three == True:
#                    gameDisplay.blit(pygame.image.load(gundamImg_list[2]), (x_red_enemie[i] - 25, y_red_enemie[i] - 25))
#
#                if difficulty == 'easy':
#                    number = 96                  
#                if difficulty == 'normal':
#                    number = 76                    
#                if difficulty == 'hard':
#                    number = 61
#                if difficulty == 'very hard':
#                    number = 41
#                if difficulty =='extreme':
#                    number = 21
#                    
#                if random.randrange(1, number) == 1:
#                    x = x_red_enemie[i]
#                    y = y_red_enemie[i]
#                    
#                    x_direction = x_player
#                    y_direction = y_player
#                    
#                    distance = sqrt((x_direction) ** 2 + (y_direction - y) ** 2)
#                    
#                    x_speed = (x_direction - x) / 240
#                    y_speed = (y_direction - y) / 240
#                    
#                    x_speed /= distance / 150
#                    y_speed /= distance / 150
#                    
#                    x_bullet_type_3_speed.append(x_speed)
#                    y_bullet_type_3_speed.append(y_speed)
#                    
#                    x_bullet_type_3.append(x)
#                    y_bullet_type_3.append(y)
#                    
#                    bullet_type_3_color.append(brightblue)
#                    
#                if x_player > x_red_enemie[i] - 25 and x_player < x_red_enemie[i] + 25 and y_player > y_red_enemie[i] - 25 and y_player < y_red_enemie[i] + 25:
#                    game_over = True
#                                    
#                if y_red_enemie[i] > 625:
#                    del x_red_enemie[i]
#                    del y_red_enemie[i]
#                    
            for i in range(len(x_blue_enemie) - 1, -1, -1):
                x_blue_enemie[i] += 2.5
                
                if mode_one == True:
                    gameDisplay.blit(pygame.image.load(touhouImg_list[3]), (x_blue_enemie[i] - 20, y_blue_enemie[i] - 15))
                if mode_two == True:
                    gameDisplay.blit(pygame.image.load(zhexueImg_list[3]), (x_blue_enemie[i] - 20, y_blue_enemie[i] - 15))
                if mode_three == True:
                    gameDisplay.blit(pygame.image.load(gundamImg_list[3]), (x_blue_enemie[i] - 20, y_blue_enemie[i] - 15))
                
                if bullet_time == 1:
                    x = x_blue_enemie[i]
                    y = y_blue_enemie[i]
                    
                    x_bullet_speed.append(0 / 30)
                    y_bullet_speed.append(-30 / 30)
                    
                    x_bullet_speed.append(22.5 / 30)
                    y_bullet_speed.append(-22.5 / 30)
                    
                    x_bullet_speed.append(30 / 30)
                    y_bullet_speed.append(0 / 30)
                    
                    x_bullet_speed.append(22.5 / 30)
                    y_bullet_speed.append(22.5 / 30)
                    
                    x_bullet_speed.append(0 / 30)
                    y_bullet_speed.append(30 / 30)
                    
                    x_bullet_speed.append(-22.5 / 30)
                    y_bullet_speed.append(22.5 / 30)
                    
                    x_bullet_speed.append(-30 / 30)
                    y_bullet_speed.append(0 / 30)
                    
                    x_bullet_speed.append(-22.5 / 30)
                    y_bullet_speed.append(-22.5 / 30)
                    
                    x_bullet.append(x)
                    y_bullet.append(y)
                    x_bullet.append(x)
                    y_bullet.append(y)
                    x_bullet.append(x)
                    y_bullet.append(y)
                    x_bullet.append(x)
                    y_bullet.append(y)
                    x_bullet.append(x)
                    y_bullet.append(y)
                    x_bullet.append(x)
                    y_bullet.append(y)
                    x_bullet.append(x)
                    y_bullet.append(y)
                    x_bullet.append(x)
                    y_bullet.append(y)
                    
                    bullet_color.append(green)
                    bullet_color.append(green)
                    bullet_color.append(green)
                    bullet_color.append(green)
                    bullet_color.append(green)
                    bullet_color.append(green)
                    bullet_color.append(green)
                    bullet_color.append(green)
                
#                if x_player > x_blue_enemie[i] - 20 and x_player < x_blue_enemie[i] + 20 and y_player > y_blue_enemie[i] - 15 and y_player < y_blue_enemie[i] + 15:
#                    game_over = True

                if x_blue_enemie[i] > 850:
                    del x_blue_enemie[i]
                    del y_blue_enemie[i]
                    
        if walk_left == True and game_over == False:
            x_player += -6
        if walk_right == True and game_over == False:
            x_player += 6
        if walk_up == True and game_over == False:
            y_player += -6
        if walk_down == True and game_over == False:
            y_player += 6

        gameDisplay.blit(player_Img, (x_player - 5, y_player - 5))
        
        if restart == True: 
            game_loop()

        if game_over == True:
            end_score.append(str(score))
            time_survive = end_score[0]
            largeText = pygame.font.Font('C:\Windows\Fonts\simkai.ttf', 250)
            TextSurf, TextRect = text_objects_darkred(death[0], largeText)
            TextRect.center = ((display_width/2), (display_height/2))
            gameDisplay.blit(TextSurf, TextRect)
            largeText = pygame.font.Font('C:\Windows\Fonts\simkai.ttf', 50)
            TextSurf, TextRect = text_objects_darkred(death[1], largeText)
            TextRect.center = ((display_width/2), (450))
            gameDisplay.blit(TextSurf, TextRect)
            largeText = pygame.font.Font('C:\Windows\Fonts\simkai.ttf', 50)
            TextSurf, TextRect = text_objects_darkred("survival score " + time_survive, largeText)
            TextRect.center = ((display_width/2), (500))
            gameDisplay.blit(TextSurf, TextRect)
            pygame.display.update()
            time.sleep(1)
            game_loop()
           
        position = {"A":[x_bullet,y_bullet],"B":[x_bullet_type_2,y_bullet_type_2],"C":[x_bullet_type_3,y_bullet_type_3],"yellow":[x_yellow_enemie,y_yellow_enemie],"green":[x_green_enemie,y_green_enemie],"red":[x_red_enemie,y_red_enemie],"blue":[x_blue_enemie,y_blue_enemie]}
        speed = {"A":[x_bullet_speed,y_bullet_speed],"B":[x_bullet_type_2,y_bullet_type_2],"C":[x_bullet_type_3,y_bullet_type_3],"yellow":[yellow_enemie_speed_x,0],"green":[0,green_enemie_speed_y],"red":[0,red_enemie_speed_y],"blue":[blue_enemie_speed_x,0]}

#        current = time.time()
#        if current > latest + interval:
#            latest = current
        evade()
                
        pygame.display.update()
        clock.tick(60)

c = 0  
#going in circles
def act():
    global c
    global walk_up
    global walk_down
    global walk_left
    global walk_right
    print(c)
    walk_up = False
    walk_down = False
    walk_left = False
    walk_right = False
    if c == 0:
        walk_left = True
    elif c == 1:
        walk_up = True
    elif c == 2:
        walk_right = True
    elif c == 3:
        walk_down = True       
    c += 1
    if c == 4:
        c = 0
        
def distance(x1,y1,x2,y2):
    return ((x1-x2)**2+(y1-y2)**2)**(1/2)

def sense():
        global position
        global speed
        x_out = []
        y_out = []
        xs_out = []
        ys_out = []
        ds_out = []
        for danger in position.keys():
            if len(position[danger][0]) > 0:
                x_lst = position[danger][0]
                y_lst = position[danger][1]
                shortest = 99999999
                for i in range(len(x_lst)):
                    x = x_lst[i]
                    y = y_lst[i]
                    cur_dist = distance(x,y,x_player,y_player)
                    try:
                        if cur_dist < shortest:
                            shortest = cur_dist
                            shortest_i = i
                    except:
                        shortest = cur_dist
                        shortest_i = i
                if danger in ["A","B","C"]:
                    xs_out.append(speed[danger][0][shortest_i])
                    ys_out.append(speed[danger][1][shortest_i])
                else:
                    xs_out.append(speed[danger][0])
                    ys_out.append(speed[danger][1])
                x_out.append(x_lst[shortest_i])
                y_out.append(y_lst[shortest_i])
                ds_out.append(shortest)
        target_i = ds_out.index(min(ds_out))
        return [x_out[target_i],y_out[target_i],xs_out[target_i],ys_out[target_i],min(ds_out)]

#logic: find the closest enemy and its direction, then evade
def evade():
    global c
    global walk_up
    global walk_down
    global walk_left
    global walk_right
    walk_up = False
    walk_down = False
    walk_left = False
    walk_right = False
    #avoid running into the wall
    if x_player > 750:
        walk_left = True
    elif x_player < 50:
        walk_right = True
    elif y_player > 550:
        walk_up = True
    elif y_player < 50:
        walk_down = True
    else:
        info = sense()
        dis = info[4]
        if dis < 100:
            #evade if danger is close
            move_vec = [info[2],info[3]]
            diff_vec = [x_player-info[0],y_player-info[1]]
            if -info[3]*diff_vec[0] + info[2]*diff_vec[1] > 0:
                normal_vec = [-info[3],info[2]]
            else:
                normal_vec = [info[3],-info[2]]
            if abs(normal_vec[0]) > abs(normal_vec[1]):
                if normal_vec[0] > 0:
                    walk_right = True
                else:
                    walk_left = True
            else:
                if normal_vec[1] > 0:
                    walk_down = True
                else:
                    walk_up = True
        else:
            #otherwise, try to get back to the center
            x_offset = 400 - x_player
            y_offset = 300 - y_player
            if abs(x_offset) > abs(y_offset):
                if x_offset > 0:
                    walk_right = True
                else:
                    walk_left = True
            else:
                if y_offset > 0:
                    walk_down = True
                else:
                    walk_up = True
            
    
#bouncing around randomly (while not hitting the wall)       
def act_random():
    global c
    global walk_up
    global walk_down
    global walk_left
    global walk_right
    sense()
    c = random.randint(0,3)
    walk_up = False
    walk_down = False
    walk_left = False
    walk_right = False
    if x_player > 750:
        walk_left = True
    elif x_player < 50:
        walk_right = True
    elif y_player > 550:
        walk_up = True
    elif y_player < 50:
        walk_down = True
    else:
        if c == 0:
            walk_left = True
        elif c == 1:
            walk_up = True
        elif c == 2:
            walk_right = True
        elif c == 3:
            walk_down = True 
    
if __name__ == "__main__":
    start()

#!/usr/bin/env python

import pygame  
from pygame._sdl2 import Window, Texture, Image, Renderer
import pygame.font
import pygame.sysfont

import math
import random

# Engine by Alexander Gnatyuk 
import sound_alex
import engine_alex
import intro_alex
import menu_alex

import utils_alex

TITLE = "Forest Trails ver0.1" 


screen_size_x=1900
screen_size_y=800


#----------------------------------------------------------------------------------------------------------------------------------------------------------
def main(winstyle=0):
    
    utils_alex.file_level_read("Level_01.map")
    pygame.display.init()
    pygame.font.init()
    pygame.sysfont.initsysfonts()

    win = Window(TITLE, (screen_size_x,screen_size_y), resizable=False)
    #win.set_icon(icon)
    #win.set_fullscreen(True)
    renderer = Renderer(win)
    
    
    sound_alex.mixer_init()
    sound_alex.muzic_play()
    

    intro=intro_alex.Intro(renderer,screen_size_x,screen_size_y)
    menu=menu_alex.Menu(renderer,screen_size_x,screen_size_y,10)

    renderer.clear()    
    engine_alex.clock = pygame.time.Clock()
    engine_alex.renderer=renderer

    
    
    #/!!!!!
    intro.action=0
        
    run=1
    try:
        while run==1:

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                                            #mouse
                                            continue
                    if event.type == pygame.KEYDOWN:
                                if engine_alex.game_mode==1:
                                                menu.set_key(event.key)
                                if engine_alex.game_mode==2:
                                                engine_alex.set_key(event.key)

                    if event.type == pygame.KEYUP:
                                if engine_alex.game_mode==2:
                                                engine_alex.clear_key(event.key)

                    if event.type == pygame.QUIT:
                                                pygame.quit()
                                                run=0
                                                break
                renderer.draw_color=(0,0,0,0)
                renderer.clear()
                if engine_alex.game_mode==0:
                            #------intro------
                            intro.show()
                            if intro.action==4:                                 
                                engine_alex.engine_init(renderer,screen_size_x,screen_size_y)
                                engine_alex.game_mode=1
                                continue                                    
                            #------intro------

                if engine_alex.game_mode==1:
                            #menu
                            menu.show()
                            



                if engine_alex.game_mode==2:
                            #------GAME------
                            engine_alex.engine()                            
                            #------GAME------

                if engine_alex.game_mode==3: break


                fps=engine_alex.update()
                win.title = str( TITLE +  "    FPS: {:.2f}".format(fps))

    finally:
        pygame.quit()

#----------------------------------------------------------------------------------------------------------------------------------------------------------
# call the "main" function if running this script
main()

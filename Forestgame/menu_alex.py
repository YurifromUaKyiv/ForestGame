
import pygame  
import math
import random
from pygame._sdl2 import Window, Texture, Image, Renderer
import pygame.font
import pygame.sysfont
import utils_alex
import engine_alex
        

Menu_str= [ "Start New Game", "Start with Level:", "Background Muzic:", "Sound:", "FPS:" , "Donate", "Exit from Game"]
#--------------------------------------------------------------------------
class Menu():
        def __init__(self, renderer, max_x, max_y, max_level):
            self.renderer=renderer
            self.max_x=max_x
            self.max_y=max_y
            self.time=0
            self.ImageMenu=[]
            self.ImageMenu.append(engine_alex.get_img(renderer,"frame.png"))   
            self.pos_x=(1900-576)/2
            self.pos_y=4
            self.index_select=0
            self.max_level=10
            self.curr_level=1
            self.muzic=True
            self.sound=True
            self.fps=60
                        
        def text_to_image(self, font, text1, text_add,  is_select):
            text=text1+text_add
            if is_select==True:  text_surface = font.render(text, True,(255, 255, 255))
            if is_select==False: text_surface = font.render(text, True,(80, 80, 80))
            txt=Texture.from_surface(self.renderer,text_surface)            
            #image=Image(txt, (0,0,txt.width, txt.height))
            return txt
            
            
        def show_menu(self):
            pygame.font.init() # Bug in Pygame!!!!
            font1 = pygame.font.SysFont("Century", 42,False)
            font2 = pygame.font.SysFont("Century", 40,True)
            width=570
            x=24
            y=150
            index=0
            for str in Menu_str:
                sel=False
                str_add=""
                font=font1
                if index==self.index_select: 
                    font=font2
                    sel=True
                if index==1: str_add='{:02d}'.format(self.curr_level)
                if index==2: 
                    str_add=" OFF"
                    if self.muzic==True:    str_add=" ON"
                if index==3: 
                    str_add=" OFF"
                    if self.sound==True:    str_add=" ON"
                    
                if index==4: str_add='{:02d}'.format(self.fps)

                txt=self.text_to_image(font, str, str_add, sel)
                image=Image(txt, (0,0,txt.width, txt.height))
                s=(width-txt.width)/2               
                image.draw(dstrect=(self.pos_x+s, self.pos_y+y))
                y+=65
                index+=1

            


        def show(self):

            engine_alex.menu_engine()

            self.ImageMenu[0].draw(dstrect=(self.pos_x, self.pos_y))
            self.show_menu()
                        


            self.time+=1
            if self.time>4: self.time=0

        def set_key(self,key):
            if key==pygame.K_UP:
                    if self.index_select>0: self.index_select-=1
            if key==pygame.K_DOWN:
                    if self.index_select<6: self.index_select+=1

            if key==pygame.K_KP_PLUS:
                    if self.curr_level<5:
                        self.curr_level+=1
            if key==pygame.K_KP_MINUS:
                    if self.curr_level>1:
                        self.curr_level-=1


            if key==pygame.K_KP_ENTER or key==pygame.K_RETURN:
                    if self.index_select==0:engine_alex.StartGame(1, True)
                    if self.index_select==1:engine_alex.StartGame(self.curr_level, True)
                    
                    if self.index_select==4:
                        if      self.fps==60: self.fps=30
                        elif    self.fps==30: self.fps=60
                        engine_alex.SetFPS(self.fps)

                    if self.index_select==6:engine_alex.ExitGame()

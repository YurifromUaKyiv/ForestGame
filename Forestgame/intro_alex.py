import pygame  
import math
import random
from pygame._sdl2 import Window, Texture, Image, Renderer
import utils_alex
import engine_alex


#--------------------------------------------------------------------------
class Intro():
        def __init__(self, renderer, max_x, max_y):
            self.renderer=renderer
            self.max_x=max_x
            self.max_y=max_y
            self.intro_time=0
            self.intro_size=8
            self.action=0
            self.curr_image=0  
            self.curr_alpha=0             
            self.ImageIntro=[]
            self.ImageIntro.append(engine_alex.get_img(renderer,"intro_au.png"))
            
            self.ImageIntro.append(engine_alex.get_img(renderer,"intro_pr.png"))
            
            self.Image = pygame.image.load(utils_alex.zip_arch("intro_fo.png"))            


        def show(self):
            pos0_x=600
            pos0_y=100
            pos1_x=560
            pos1_y=350
            pos2_x=80
            pos2_y=80

            self.intro_time+=1


            if self.action==0:
                                        self.ImageIntro[0].alpha=self.curr_alpha
                                        #self.ImageIntro[1].alpha=0
                                        self.ImageIntro[0].draw(dstrect=(pos0_x, pos0_y))
                                        if self.curr_alpha<250: 
                                            self.curr_alpha+=2
                                        if self.curr_alpha>=250: 
                                                self.action=1
                                                self.curr_alpha=1
                                        

            if self.action==1:                
                                        self.ImageIntro[0].alpha=250                                        
                                        self.ImageIntro[1].alpha=self.curr_alpha
                                        self.ImageIntro[0].draw(dstrect=(pos0_x, pos0_y))
                                        self.ImageIntro[1].draw(dstrect=(pos1_x, pos1_y))

                                        if self.curr_alpha<250: 
                                            self.curr_alpha+=1
                                        if self.curr_alpha>=250: self.action=2
                                        if self.intro_time>1: self.intro_time=0

            if self.action==2:                
                                        self.ImageIntro[0].alpha=self.curr_alpha                                        
                                        self.ImageIntro[1].alpha=self.curr_alpha
                                        self.ImageIntro[0].draw(dstrect=(pos0_x, pos0_y))
                                        self.ImageIntro[1].draw(dstrect=(pos1_x, pos1_y))

                                        if self.curr_alpha>=10 and self.intro_time>2: self.curr_alpha-=5
                                        if self.curr_alpha<10: self.action=3
                                        if self.intro_time>2: self.intro_time=0

            if self.action>=3: 
                                        if self.intro_size-400<self.Image.get_width(): self.intro_size+=6
                                        else:  self.action=4

                                        position_x=(self.max_x- self.intro_size) / 2
                                        position_y=(self.max_y- self.intro_size/2) / 2
                                        tmp=pygame.transform.scale(self.Image, (self.intro_size, self.intro_size/2))
                                        
                                        self.texture = Texture.from_surface(self.renderer, tmp)                                        
                                        image=Image(self.texture, (0,0,self.texture.width, self.texture.height))
                                        image.draw(dstrect=(position_x, position_y))


                                        #self.ImageIntro[2].draw(dstrect=(pos2_x, pos2_y))



#--------------------------------------------------------------------------


                
               


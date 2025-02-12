import pygame  
import math
import random
from pygame._sdl2 import Window, Texture, Image, Renderer
import sound_alex
import maps_engine
import utils_alex

MAN_X=200
MAN_Y=635

sky_max_x=2000
sky_max_y=1000

sprites_delay=20

global mySky
global myHero
global engineBlood
global engineLevel

global myKey_lr
global myKey_ud
global myKey_wx

global myMagic
myRockets=[]
myCartridge=[]

game_mode=0  # 0 - 1 - 2
global clock
global renderer
FPS = 60 



#--------------------------------------------------------------------------
def img_to_text(rend, file):
                img=pygame.image.load(utils_alex.zip_arch(file))
                tmp=pygame.transform.scale(img, (26*2, 36*2))
                txt=Texture.from_surface(rend,tmp)
                image=Image(txt, (0,0,txt.width, txt.height))
                image.blend_mode=1
                return image
#--------------------------------------------------------------------------
def img_to_text64(rend, file):
                img=pygame.image.load(utils_alex.zip_arch(file))
                tmp=pygame.transform.scale(img, (64, 64))
                txt=Texture.from_surface(rend,tmp)
                image=Image(txt, (0,0,txt.width, txt.height))
                image.blend_mode=1
                return image
#--------------------------------------------------------------------------

def img_to_mask(rend, file):
                img=pygame.image.load(utils_alex.zip_arch(file))
                tmp=pygame.transform.scale(img, (26*2, 36*2))
                mask = pygame.mask.from_surface(tmp)
                return mask
#--------------------------------------------------------------------------
def get_img(rend, file):
                img=pygame.image.load(utils_alex.zip_arch(file))                
                txt=Texture.from_surface(rend,img)
                image=Image(txt, (0,0,txt.width, txt.height))
                image.blend_mode=1
                return image
#--------------------------------------------------------------------------


class EngineHero():
        def __init__(self, x,y, renderer):
            self.renderer=renderer
            self.curr_time=0
            self.curr_alpha=255  

            self.image_idle=[]
            self.image_run=[]
            self.image_climb=[]
            self.image_attack=[]
            self.image_dies=[]

            self.image_score=[]

            self.image_bow=[]
                       
            #image idle
            self.image_idle.append(img_to_text(renderer,"man_idle1.png"))
            self.image_idle.append(img_to_text(renderer,"man_idle2.png"))
            self.image_idle.append(img_to_text(renderer,"man_idle3.png"))
            self.image_idle.append(img_to_text(renderer,"man_idle4.png"))
            self.image_idle_max=3

            #image run
            self.image_run.append(img_to_text(renderer,"man_run1.png"))
            self.image_run.append(img_to_text(renderer,"man_run2.png"))
            self.image_run.append(img_to_text(renderer,"man_run3.png"))
            self.image_run.append(img_to_text(renderer,"man_run4.png"))
            self.image_run.append(img_to_text(renderer,"man_run5.png"))
            self.image_run.append(img_to_text(renderer,"man_run6.png"))
            self.image_run_max=5

            #image climb
            self.image_climb.append(img_to_text(renderer,"man_climb1.png"))
            self.image_climb.append(img_to_text(renderer,"man_climb2.png"))
            self.image_climb.append(img_to_text(renderer,"man_climb3.png"))
            self.image_climb.append(img_to_text(renderer,"man_climb4.png"))
            self.image_climb.append(img_to_text(renderer,"man_climb5.png"))
            self.image_climb.append(img_to_text(renderer,"man_climb6.png"))
            self.image_climb_max=5

            #image attack
            self.image_attack.append(img_to_text(renderer,"man_attack6.png"))
            self.image_attack.append(img_to_text(renderer,"man_attack5.png"))
            self.image_attack.append(img_to_text(renderer,"man_attack4.png"))
            self.image_attack.append(img_to_text(renderer,"man_attack3.png"))
            self.image_attack.append(img_to_text(renderer,"man_attack2.png"))
            self.image_attack.append(img_to_text(renderer,"man_attack1.png"))
            self.image_attack_max=5

            #image dies
            self.image_dies.append(img_to_text(renderer,"man_dies1.png"))
            self.image_dies.append(img_to_text(renderer,"man_dies2.png"))
            self.image_dies.append(img_to_text(renderer,"man_dies3.png"))
            self.image_dies.append(img_to_text(renderer,"man_dies4.png"))
            self.image_dies.append(img_to_text(renderer,"man_dies5.png"))
            self.image_dies.append(img_to_text(renderer,"man_dies6.png"))
            self.image_dies_max=5


            self.image_score.append(get_img(renderer,"frame_zero.png"))

            self.image_bow.append(get_img(renderer,"longbow.png"))
            self.image_bow.append(get_img(renderer,"crossbow.png"))
            
            self.position_x=x
            self.position_y=y
            self.spites_idle=0            
            self.spites_run=0            
            self.spites_climb=0            
            self.spites_attack=0  
            self.spites_dies=0  
            self.delay=sprites_delay
            self.left_right=0
            self.up_down=0
            self.FlipX=0
            self.State=0
            self.JumpEnergy=64
            self.FreeFallEnergy=0
            self.Shooting=0

            self.Score_Heart=100
            self.Score_Ammo=100
            self.Score_Monster=0
            self.Score_Arrows=200
            self.Score_Gun_angle=0

            self.current_Gun=1
            
    
            
            #self.mask1=img_to_mask(renderer,"man_idle1.png")
            #self.mask2=img_to_mask(renderer,"shot.png")

            #over=self.mask1.overlap_area(self.mask1, (140,50))
            #if over>0:

#----------------------------------------------------------------------------------------------
        def flip_image(self, st):
            for i in range(self.image_idle_max+1):
                    self.image_idle[i].flip_x=st
            for i in range(self.image_run_max+1):
                    self.image_run[i].flip_x=st
           
#----------------------------------------------------------------------------------------------
        def no_change(self):            
            if self.left_right>0:
                    self.left_right-=1
            if self.left_right<0:
                    self.left_right+=1
                
            if self.up_down>0:
                    self.up_down-=1
            if self.up_down<0:
                    self.up_down+=1

            if  self.State==1 and self.left_right==0 and self.up_down==0:
                        self.State=0

                
#----------------------------------------------------------------------------------------------
        def change(self, new):
                    if self.State==10: return 
                    if self.State==11: return 

                    if (new==1 or new==-1) and self.State==2:
                        if (engineLevel.dw1>1 and engineLevel.mid1==0 and engineLevel.sh1==0) or (engineLevel.dw2>1 and engineLevel.mid2==0 and engineLevel.sh2==0) or (engineLevel.dw3>1 and engineLevel.mid3==0 and engineLevel.sh3==0):
                            self.State=1
                            if new==-1 :
                                self.left_right=-15
                                self.position_x-=4
                            if new==1 :
                                self.left_right=15
                                self.position_x+=4
                            #635+32
                            self.position_y=(int)(engineLevel.up1_y )+27 
                        elif new==-1 and  engineLevel.dw1==0 and engineLevel.mid1==0 and engineLevel.sh1==0:
                            self.State=1
                            self.left_right=-15
                            self.position_x-=4
                        elif new==1 and  engineLevel.dw3==0 and engineLevel.mid3==0 and engineLevel.sh3==0:
                            self.State=1
                            self.left_right=15
                            self.position_x+=4

                    if self.FlipX!=1:
                                    if self.State<2 and new==1: #rigth
                                        self.State=1
                                        self.left_right+=2         
                                        if self.left_right>100:
                                            self.left_right=100
                                        self.up_down=0
                                            
                                    if self.State<2 and new==-1: #left
                                        self.State=1
                                        self.left_right-=2         
                                        if self.left_right<-100:
                                            self.left_right=-100
                                        self.up_down=0    
                    else:
                                    if self.State<2 and new==1: #rigth
                                        self.State=1
                                        self.left_right+=2         
                                        if self.left_right>100:
                                            self.left_right=100
                                        self.up_down=0
                                            
                                    if self.State<2 and new==-1: #left
                                        self.State=1
                                        self.left_right-=2         
                                        if self.left_right<-100:
                                            self.left_right=-100                                            
                                        self.up_down=0
                                    
                    if self.State<3 and new==2: #down
                        if engineLevel.dw1==1 or engineLevel.dw2==1 or engineLevel.dw3==1 or engineLevel.sh1==1 or engineLevel.sh2==1 or engineLevel.sh3==1  :
                            if engineLevel.dw1==1: 
                                if self.State!=2 : self.position_x=engineLevel.dw1_x-engineLevel.engineMaps.MapScrollX-8
                            elif engineLevel.dw2==1: 
                                if self.State!=2 : self.position_x=engineLevel.dw2_x-engineLevel.engineMaps.MapScrollX-8
                            elif engineLevel.dw3==1: 
                                if self.State!=2 : self.position_x=engineLevel.dw3_x-engineLevel.engineMaps.MapScrollX-8

                            
                            self.State=2
                            self.up_down+=1         
                            if self.up_down>100:
                                self.up_down=100
                            self.left_right=0
                            
                    if self.State<5 and new==-2: #up
                        if engineLevel.up1==1 or engineLevel.up2==1 or engineLevel.up3==1 or engineLevel.mid1==1 or engineLevel.mid2==1 or engineLevel.sh1==1 or engineLevel.sh2==1 or engineLevel.dw1==1 or engineLevel.dw2==1:
                            if engineLevel.up1==1: 
                                if self.State!=2 : self.position_x=engineLevel.up1_x-engineLevel.engineMaps.MapScrollX-8
                            elif engineLevel.up2==1:
                                if self.State!=2 : self.position_x=engineLevel.up2_x-engineLevel.engineMaps.MapScrollX-8
                            elif engineLevel.up3==1:
                                if self.State!=2 : self.position_x=engineLevel.up3_x-engineLevel.engineMaps.MapScrollX-8
                            
                            self.State=2
                            self.up_down-=1         
                            if self.up_down<-100:
                                self.up_down=-100  
                            self.left_right=0

                    if self.left_right>0:
                        self.FlipX=0                    
                    if self.left_right<0:
                        self.FlipX=1

                    if self.State==1 and self.left_right==0 and self.up_down==0:
                            self.State=0
                    
                    if self.FlipX==1:
                                self.flip_image(True)
                    else:
                                self.flip_image(False)
                                
#----------------------------------------------------------------------------------------------
#                    
        def check_position_hero(self):
            if self.State==10: return 
            if self.State==11: return 
            if self.Score_Heart<=0:
                self.State=10
                self.spites_dies=0
                return


            if self.State==-1 and (engineLevel.dw1==0 or engineLevel.dw1==1)  and (engineLevel.dw2==0 or engineLevel.dw2==1):
                self.State=4 # Free Fall
                self.FreeFallEnergy=0

            if self.State==1 and (engineLevel.dw1==0 or engineLevel.dw1==1)  and (engineLevel.dw2==0 or engineLevel.dw2==1) and (engineLevel.dw3==0 or engineLevel.dw3==1):
                self.State=4 # Free Fall
                self.FreeFallEnergy=0
            if engineLevel.sh2==0 and engineLevel.sh3==0 and engineLevel.dw2==0 and engineLevel.dw3==0:
                self.State=4 # Free Fall
                self.FreeFallEnergy=0
            
            if self.State==0 and (engineLevel.dw2==0 or engineLevel.dw2==1) and (engineLevel.dw3==0 or engineLevel.dw3==1):
                self.State=4 # Free Fall
                self.FreeFallEnergy=0

            if self.State==0 and (engineLevel.dw1==0 or engineLevel.dw1==1) and (engineLevel.dw2==0 or engineLevel.dw2==1):
                self.State=4 # Free Fall
                self.FreeFallEnergy=0


            if (engineLevel.sh3==3 and  self.left_right>80) or (engineLevel.sh2==3 and  self.left_right>80) or ( engineLevel.mid3==3 and  self.left_right>80) or ( engineLevel.dw3==3 and  self.left_right>80):
                self.State=3
                self.JumpEnergy=8
                self.position_y-=8
            if (engineLevel.sh1==2 and  self.left_right<-80) or (engineLevel.mid1==2 and  self.left_right<-80) or ( engineLevel.dw1==2 and  self.left_right<-80):
                self.State=3
                self.JumpEnergy=8
                self.position_y-=8

            if (engineLevel.sh2==3 and self.State!=3):
                self.JumpEnergy=16
#Free Fall State==4
#Jump State==3
#Climb State==2
#Run State==1
#Idle State==0
#Die==10
#Level Complete ==11
            if engineLevel.sh1==97 or engineLevel.sh3==97 or engineLevel.mid1==97 or engineLevel.mid3==97:
                #exit
                if engineLevel.monster_count==0:
                    #level complete
                    self.State=11
                    return
                    


            die_array=[175,198,199,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,314,315,316,317]
            die=0
            if self.State==-1 or self.State==1 or self.State==0 or self.State==4:
                for bad1 in die_array:
                    if engineLevel.dw1==bad1:
                        for bad2 in die_array:
                            if engineLevel.dw2==bad2:
                                for bad3 in die_array:
                                    if engineLevel.dw3==bad3:
                                         die=1
                                         sound_alex.sound_pain()
                                         self.FreeFallEnergy=0
                                         h_x=self.position_x
                                         h_y=self.position_y
                                         engineBlood.add_obj(h_x-3,h_y+10,random.randrange(0,29,1))
                                         engineBlood.add_obj(h_x,h_y+23,random.randrange(0,29,1))
                                         engineBlood.add_obj(h_x+3,h_y+33,random.randrange(0,29,1))
                                         break
            if die>0: 
                self.State=10
                self.spites_dies=0
                self.Score_Heart=0

#----------------------------------------------------------------------------------------------
        def show(self, scrll):
                    self.position_x-=scrll
                    engineLevel.MapGetObjs(self.position_x, self.position_y, 32,72,scrll)
                    if self.State!=2 and  self.State!=4 and  self.State!=3: self.check_position_hero() # check Free Fall
                    engineLevel.MapScrollingAnalyze(self.position_x,self.position_y)

                    self.delay-=1
                    if self.delay<=0:
                        self.delay=sprites_delay                        
                        self.spites_idle+=1
                        if self.spites_idle>self.image_idle_max:
                            self.spites_idle=0
                        
                        self.spites_run+=1
                        self.spites_climb+=1            
                        self.spites_attack+=1  
                        self.spites_dies+=1

                        if self.spites_run>self.image_run_max:
                            self.spites_run=0
                        if self.spites_climb>self.image_climb_max:
                            self.spites_climb=0
                        if self.spites_attack>self.image_attack_max:
                            self.spites_attack=0
                    
                    step_x=0
                    step_y=0
#-------------------    
                    if self.left_right!=0:
                                        step_x=self.left_right/15

                    # Shoting
                    if self.Shooting>0:
                            self.image_attack[self.Shooting].flip_x=self.FlipX
                            self.image_attack[self.Shooting].draw(dstrect=(self.position_x, self.position_y))
                            if self.delay==sprites_delay:self.Shooting+=1
                            if self.Shooting>=self.image_attack_max: self.Shooting=0
                            
                    # Die
                    if self.State==10:
                        if self.spites_dies>=self.image_dies_max: 
                            self.spites_dies=self.image_dies_max
                        else: 
                            self.position_y+=0.4
                        self.image_dies[self.spites_dies].draw(dstrect=(self.position_x, self.position_y))

                
                    #Free Fall State==4
                    if self.State==4:
                        step_y=4
                        self.FreeFallEnergy+=1                        
                       
                        if step_x<0:
                            if engineLevel.dw1>1 and engineLevel.dw2>1:
                                self.State=0
                                step_y=0

                                # Heart
                                if  self.FreeFallEnergy>50:
                                        self.Score_Heart-=(self.FreeFallEnergy-50)
                                        if self.Score_Heart<0: self.Score_Heart=0
                                        sound_alex.sound_pain()
                                        self.FreeFallEnergy=0
                                        h_x=self.position_x
                                        h_y=self.position_y
                                        engineBlood.add_obj(h_x-3,h_y+23,random.randrange(0,29,1))
                                        engineBlood.add_obj(h_x,h_y+20,random.randrange(0,29,1))
                                        engineBlood.add_obj(h_x+3,h_y+23,random.randrange(0,29,1))

                            if engineLevel.sh1>1 or engineLevel.mid1>1 :  
                                step_x=0                                                                
                            if self.position_x>32: self.position_x+=step_x
                        elif step_x>=0 :
                                if engineLevel.dw1>1  and  engineLevel.dw2>1:
                                    self.State=0
                                    step_y=0
                                    # Heart
                                    if  self.FreeFallEnergy>50:
                                        self.Score_Heart-=(self.FreeFallEnergy-50)
                                        if self.Score_Heart<0: self.Score_Heart=0
                                        sound_alex.sound_pain()
                                        self.FreeFallEnergy=0
                                        h_x=self.position_x
                                        h_y=self.position_y
                                        engineBlood.add_obj(h_x-3,h_y+20,random.randrange(0,29,1))
                                        engineBlood.add_obj(h_x,h_y+23,random.randrange(0,29,1))
                                        engineBlood.add_obj(h_x+3,h_y+23,random.randrange(0,29,1))

                                if engineLevel.mid2>1 or engineLevel.mid3>1:  
                                     step_x=0                                                                                                      
                                if self.position_x<1900-32:  self.position_x+=step_x
                        
                        if self.position_y<800-16: 
                             self.position_y+=step_y

                        
                        if self.Shooting==0: 
                            if self.FlipX==0 : self.image_dies[2].draw(dstrect=(self.position_x, self.position_y))
                        if self.Shooting==0: 
                            if self.FlipX==1 : self.image_run[2].draw(dstrect=(self.position_x, self.position_y))
                        return


                    #Jump State==3
                    if self.State==3:
                        self.JumpEnergy-=2;
                        step_y=-4
                        if self.JumpEnergy<0:
                            self.State=0
                        if step_x<0:
                            if engineLevel.up1>1 or engineLevel.mid1>1 :  
                                step_x=0
                                step_y=0
                            if self.position_x>32: self.position_x+=step_x
                        elif step_x>0 :
                             if engineLevel.up2>1 or engineLevel.mid2>1 or engineLevel.mid3>3:  
                                 step_x=0
                                 step_y=0
                             if self.position_x<1900-32: 
                                                    self.position_x+=step_x
                        elif step_x==0 :
                             if engineLevel.mid2>1:  
                                 step_x=0
                                 step_y=0
                             if self.position_x<1900-32: 
                                                    self.position_x+=step_x
                        if self.position_y>8: 
                                                    self.position_y+=step_y
                        if self.Shooting==0: self.image_run[0].draw(dstrect=(self.position_x, self.position_y))
                        return

                    #Jump end
                    
                    if step_x<0:
                                if engineLevel.mid1>1 or engineLevel.sh1>1 :  
                                    step_x=0
                                    self.left_right=0
                                if self.position_x>32: 
                                                    self.position_x+=step_x
#-------------------
                    if step_x>=0 :
                                if engineLevel.mid2>1 or engineLevel.mid3>1 or engineLevel.sh3>1 :  
                                    step_x=0
                                    self.left_right=0
                                if self.position_x<1900-32: 
                                                    self.position_x+=step_x
                
                    if self.up_down!=0:
                                 step_y=self.up_down/sprites_delay

                    if step_y<0 :
                                if engineLevel.up1==1 or engineLevel.up2==1 or engineLevel.mid1==1 or engineLevel.mid2==1 or engineLevel.sh2==1:
                                    if self.position_y>8: 
                                                    self.position_y+=step_y

                    if step_y>=0:
                                if engineLevel.dw1==1 or engineLevel.dw2==1 or ((engineLevel.dw1==0 or engineLevel.dw2==0) and (engineLevel.mid1==1 or engineLevel.mid2==1)) or ((engineLevel.dw1==0 or engineLevel.dw2==0) and (engineLevel.sh1==1 or engineLevel.sh2==1)):
                                    if self.position_y<800-16: 
                                                    self.position_y+=step_y

                    if self.position_y<500:
                                            engine_sky_up_down(-1)
                    if self.position_y>600:
                                            engine_sky_up_down(1)

                    #state
                    if self.State==0:
                        if self.Shooting==0: self.image_idle[self.spites_idle].draw(dstrect=(self.position_x, self.position_y))

                    if self.State==1:
                        if self.Shooting==0: self.image_run[self.spites_run].draw(dstrect=(self.position_x, self.position_y))
                        if step_x>0:
                            self.delay-=step_x
                        if step_x<0:
                            self.delay+=step_x

                    if self.State==2:
                        if self.Shooting==0: self.image_climb[self.spites_climb].draw(dstrect=(self.position_x, self.position_y))
                        if step_y>0:
                            self.delay-=step_y
                        if step_y<0:
                            self.delay+=step_y
                        if step_y==0:
                            self.delay=sprites_delay

                    #self.Shooting
                    if self.Shooting>=self.image_attack_max: self.Shooting=0
                        
#-------------------------------------------------------------------------- 
#Free Fall State==4
#Jump State==3
#Climb State==2
#Run State==1
#Idle State==0


        def Jump(self):
            if self.State==3 or self.State==2 or self.State>3: return
            self.State=3
            self.JumpEnergy=48
            sound_alex.sound_jump()
                    
  
        def Ammo(self):            
            if self.State==2 or self.State==10 : return  #Climb State==2
            if self.current_Gun==0:
                if self.Score_Ammo>0:
                    self.Score_Ammo-=1
                else: 
                    sound_alex.sound_ammo_null()
                    return

                self.Shooting=1     
                cartridge_add(self.current_Gun)
                sound_alex.sound_shot1()
                    
            if self.current_Gun==1:
                if self.Score_Arrows>0:
                    self.Score_Arrows-=1
                else: 
                    sound_alex.sound_ammo_null()
                    return

                self.Shooting=1     
                cartridge_add(self.current_Gun)
                sound_alex.sound_arrow()
                   
#--------------------------------------------------------------------------  
        def score(self, level, heart, arrows,  ammo, gun_angle, monster, alpha ):
            pygame.font.init() # Bug in Pygame!!!!
            font = pygame.font.SysFont("Consolas", 18, True)
            self.image_score[0].draw(dstrect=(0, 780))

            self.image_bow[self.current_Gun].draw(dstrect=(3, 777))

            str_level=' Level:{:02d}'.format(level)
            str_heart=' Heart:{:03d}'.format(heart)
            str_arrows= ' Arrows:{:03d}'.format(arrows)
            str_ammo= ' Ammo:{:03d}'.format(ammo)
            if gun_angle>=0: str_gun_angle= ' Gun angle:+{:02d}'.format(int(gun_angle))
            if gun_angle<0:  str_gun_angle= ' Gun angle:{:03d}'.format(int(gun_angle))
            str_mons= '  Monster:{:02d}'.format(monster)
            text=str_level+str_heart+str_arrows+str_ammo+str_gun_angle+str_mons
            text_surface=font.render(text, True,(255, 255, 255))
            txt=Texture.from_surface(self.renderer,text_surface)
            image=Image(txt, (0,0,txt.width, txt.height))                
            image.draw(dstrect=(32, 782))
            if alpha<200:
                font = pygame.font.SysFont("Consolas", 120, True)
                text_surface=font.render(str_level, True,(255, 255, 0))
                txt=Texture.from_surface(self.renderer,text_surface)
                image=Image(txt, (0,0,txt.width, txt.height))                
                image.draw(dstrect=((1900-txt.width)/2, 300))

#--------------------------------------------------------------------------  
        def complete(self):
            pygame.font.init() # Bug in Pygame!!!!
            font = pygame.font.SysFont("Consolas", 120, True)
            text_surface=font.render("Level Complete!", True,(255, 255, 0))
            txt=Texture.from_surface(self.renderer,text_surface)
            image=Image(txt, (0,0,txt.width, txt.height))                
            image.draw(dstrect=((1900-txt.width)/2, 300))


#--------------------------------------------------------------------------  
        def check(self):
                    #mask=self.mask[self.spites]                 
                    return 0

class EngineImage():
        def __init__(self, file, renderer):
            self.renderer=renderer
            self.curr_time=0
            self.curr_alpha=255                                  
            self.image = pygame.image.load(utils_alex.zip_arch(file))
            self.texture = Texture.from_surface(self.renderer, self.image)
            self.texture.blend_mode=1
            self.position_x=0
            self.position_y=0
            self.max_x=0
            self.max_y=0
            self.count=0
            self.up=0
#--------------------------------------------------------------------------      



def engine_sky(alpha): #2000 x 1000
        mySky.count+=1
        mySky.curr_alpha=alpha
        if mySky.count>8:
                mySky.count=0 
                mySky.position_x-=1
                if mySky.up < 0:
                    if mySky.position_y<0:
                            mySky.position_y+=1
                if mySky.up > 0:
                    if mySky.position_y>-200:
                            mySky.position_y-=1
                            

        mySky.texture.alpha=mySky.curr_alpha
        mySky.texture.draw(dstrect=(mySky.position_x, mySky.position_y))
        delta=sky_max_x-mySky.max_x #520
        if mySky.position_x<=(- (delta)):
            mySky.texture.draw(dstrect=(mySky.position_x+2000, mySky.position_y))
            

        if mySky.position_x<=(-sky_max_x):
            mySky.position_x=0

#-----------------------------------------------------------------------------------------------                    
def engine_sky_up_down(up):
        mySky.up=up
#-----------------------------------------------------------------------------------------------
def engine_hero(scrll):
        global myHero 
        global myKey_lr
        global myKey_ud
        global myKey_wx

        myHero.show(scrll)

        if myKey_lr!=0:
            if myKey_lr==pygame.K_LEFT:
                myHero.change(-1)
            if myKey_lr==pygame.K_RIGHT:
                myHero.change(1)
        if myKey_ud!=0:                
            if myKey_ud==pygame.K_UP:
                myHero.change(-2)
            if myKey_ud==pygame.K_DOWN:
                myHero.change(2)
        if myKey_lr==0 and myKey_ud==0:
            myHero.no_change()

        if myKey_wx==pygame.K_q:
            if myHero.Score_Gun_angle<60: myHero.Score_Gun_angle+=0.5
        if myKey_wx==pygame.K_a:
            if myHero.Score_Gun_angle>-60: myHero.Score_Gun_angle-=0.5

        
        myHero.check()
        
        

#-----------------------------------------------------------------------------------------------
def engine_heli_change(a):
        global myHero
        myHero.change(a)

#-----------------------------------------------------------------------------------------------
class SpriteCartridge():
        def __init__(self,image, x,y,angle,direction):
            self.curr_time=0
            self.curr_alpha=255                                  
            self.position_x=x+0.00
            self.position_y=y+0.00
            self.max_x=0
            self.max_y=0
            self.radius=0
            self.image_gun=image
            if direction==0: self.angle=-angle
            if direction==1: self.angle=angle
            self.direction=direction
            self.power_y=0


def cartridge_add(image_gun):
    if myHero.FlipX==0:
        myCartridge.add(image_gun, myHero.position_x+33,   myHero.position_y+24,  myHero.Score_Gun_angle , myHero.FlipX )
    else:
        myCartridge.add(image_gun, myHero.position_x,      myHero.position_y+24,  myHero.Score_Gun_angle, myHero.FlipX )

def cartridge_more_add():
        for x in range(40):
            angle=x*9
            myCartridge.add(myHero.position_x,myHero.position_y,angle, 0 )
    
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
class EngineCartridge():
        def __init__(self, file1, file2, renderer):
            self.renderer=renderer

            image = pygame.image.load(utils_alex.zip_arch(file1))
            texture = Texture.from_surface(self.renderer, image)
            texture.blend_mode=1
            self.image_ammo=Image(texture, (0,0,texture.width, texture.height))
            self.image_ammo.blend_mode=1

            self.image=self.image_ammo

            image = pygame.image.load(utils_alex.zip_arch(file2))
            texture = Texture.from_surface(self.renderer, image)
            texture.blend_mode=1
            self.image_arrow=Image(texture, (0,0,texture.width, texture.height))
            self.image_arrow.blend_mode=1


            self.cartridges=[]

        def add(self, image, x,y,angle,direction ):
            sprite=SpriteCartridge(image, x,y,angle,direction)
            self.cartridges.append(sprite)

        def check_monstr(sefl, x,y):
                global engineBlood
                global engineLevel
                ret=0

                ScrollX = (engineLevel.engineMaps.MapStartPositionW*32)+engineLevel.engineMaps.MapScrollX;
                ScrollY = engineLevel.engineMaps.MapScrollY
                for i in range(engineLevel.engineHeroes.HeroesCount):
                    objs=engineLevel.engineHeroes.myHeroes[i]
                    obj=objs[0]
                    p_x=objs[1] - ScrollX
                    p_y=objs[2] - ScrollY
                    heart=objs[3]
                    state=objs[4]
                    if state!=0: continue
                    if p_x < x + 16 and  p_y+4 < y + 16 and p_x + 25 > x and  p_y + 65 > y:
                        heart-=10
                        objs[3]=heart
                        a_x=random.randrange(0,20,1)                       
                        engineBlood.add_obj_monstr(p_x+ScrollX+a_x,    p_y-8+ScrollY,random.randrange(0,29,1))                        
                        a_x=random.randrange(10,20,1)                       
                        engineBlood.add_obj_monstr(p_x+ScrollX+a_x,    p_y+8+ScrollY,random.randrange(0,29,1))                        
                        sound_alex.sound_pain_monstr()
                        a_x=random.randrange(15,20,1)                       
                        engineBlood.add_obj_monstr(p_x+ScrollX+a_x,    p_y+16+ScrollY,random.randrange(0,29,1))                        

                        if heart<=0:
                            objs[4]=random.randrange(1,5,1)
                        ret=1
                
                return ret



        def show(self,scrll):
             ccc=len(self.cartridges)
             if ccc>0 and ccc<20:
                        ccc=0
             for r in self.cartridges: 
                    
                    if r.image_gun==0:  self.image=self.image_ammo 
                    if r.image_gun==1:  self.image=self.image_arrow

                    self.image.angle=r.angle

                    if r.direction==1:
                        self.image.flip_x=True
                    else:
                        self.image.flip_x=False
                                  
                    if r.direction==0:
                                if r.image_gun==0:  r.radius+=10                                
                                else:               r.radius+=7                                
                                angle=0
                                if r.angle<0:
                                        angle=-r.angle
                                else:
                                        angle=360-r.angle

                                radian=(angle*3.14159/180)
                                x = r.radius*math.cos(radian)
                                y = r.radius*math.sin(radian)

                                if r.image_gun==1:  
                                    r.angle+=0.1
                                    r.power_y+=0.001
                                    r.position_y+=r.power_y
                                    
                                
                                self.image.draw(dstrect=(r.position_x+x-scrll, r.position_y-y))
                                if self.check_monstr(r.position_x+x, r.position_y-y)==1:
                                    self.cartridges.remove(r)
                                    continue

                                if r.position_x+x>3500:
                                            self.cartridges.remove(r)
                                            continue
                                if r.position_x+x<-1500:
                                            self.cartridges.remove(r)
                                            continue
                                if r.position_y-y<-100:
                                            self.cartridges.remove(r)
                                            continue
                                if r.position_y-y>1000:
                                            self.cartridges.remove(r)
                                            continue


                    if r.direction==1:
                                if r.image_gun==0:  r.radius+=10                                
                                else:               r.radius+=7                                

                                angle=0
                                if r.angle<0:
                                        angle=-r.angle
                                else:
                                        angle=360-r.angle

                                radian=(angle*3.14159/180)
                                x = r.radius*math.cos(radian)
                                y = r.radius*math.sin(radian)

                                if r.image_gun==1:  
                                    r.angle-=0.1
                                    r.power_y+=0.001
                                    r.position_y+=r.power_y

                                
                                self.image.draw(dstrect=(r.position_x-x, r.position_y+y))
                                if self.check_monstr(r.position_x-x, r.position_y+y)==1:
                                    self.cartridges.remove(r)
                                    continue


                                if r.position_x-x<-100:
                                            self.cartridges.remove(r)
                                            continue
                                if r.position_y+y<-100:
                                            self.cartridges.remove(r)
                                            continue
                                if r.position_y+y>1000:
                                            self.cartridges.remove(r)
                                            continue

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
class SpriteMagic():
        def __init__(self,x,y,sprite, index, angle, direction):
            self.curr_time=0 
            self.sprite=sprite
            self.position_x=x+0.00
            self.position_y=y+0.00
            self.angle=angle
            self.w_angle=0.00
            self.direction=direction            
            self.delay=0
            self.power_x=random.randrange(5, 15, 1)
            self.power_y=random.randrange(-3, 3, 1)
            self.radius=0
            self.index=index
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
class SpriteArrow():
        def __init__(self,x,y,sprite, index,  angle, direction):
            self.curr_time=0 
            self.sprite=sprite
            self.position_x=x+0.00
            self.position_y=y+0.00
            self.angle=angle            
            self.direction=direction            
            self.delay=0
            self.power_x=random.randrange(3, 7, 1)
            self.power_y=random.randrange(-3, 3, 1)
            if direction==-1:
                self.power_x=8
                self.power_y=0

            self.radius=0
            self.index=index
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
class EngineMagic():
            def __init__(self, renderer):
                self.ImageMag=[]
                self.ImageArrow=[]
                self.ImageMag.append(get_img(renderer,"cloud_acid_2.png"))
                self.ImageMag.append(get_img(renderer,"cloud_chaos_2.png"))
                self.ImageMag.append(get_img(renderer,"cloud_cold_2.png"))
                self.ImageMag.append(get_img(renderer,"cloud_forest_fire.png"))
                self.ImageMag.append(get_img(renderer,"cloud_meph_2.png"))
                self.ImageMag.append(get_img(renderer,"cloud_rain_2.png"))
                self.ImageMag.append(get_img(renderer,"cloud_storm_1.png"))
                self.ImageMag.append(get_img(renderer,"searing_ray_4.png"))

                self.ImageArrow.append(get_img(renderer,"arrow_6.png"))
                self.ImageArrow.append(get_img(renderer,"bolt6.png"))
                self.ImageArrow.append(get_img(renderer,"dart6.png"))
                self.ObjMagic=[]
                self.ObjArrow=[]                
                self.TimeRepit=400

            def add_magic(self, x,y,sprite, index):
                angle=random.randrange(170, 190,1)
                obj=SpriteMagic(x,y,sprite,index, angle,0)
                self.ObjMagic.append(obj)

            def add_arrow(self, x,y,sprite, index):
                angle=random.randrange(170, 190,1)
                obj=SpriteArrow(x,y,sprite, index, angle,0)
                self.ObjArrow.append(obj)

            def add_arrow_cycle(self, x,y,sprite, index,angle):
                obj=SpriteArrow(x,y,sprite, index, angle,-1)
                self.ObjArrow.append(obj)
            
            def nnnnn(self,a):
                if a==1: return



            def check_is_hero(self, image, x,y, obj):
                ret=0
                #get pos_hero 26*2 36*2
                global myHero
                h_x=myHero.position_x
                h_y=myHero.position_y

                if h_x < x + 16 and  h_y+4 < y + 16 and h_x + 25 > x and  h_y + 65 > y:
                    if obj==0:   myHero.Score_Heart-=1
                    if obj==1:   myHero.Score_Heart-=1
                    if obj==2:   myHero.Score_Heart-=1
                    if obj==3:   myHero.Score_Heart-=3
                    if obj==4:   myHero.Score_Heart-=4
                    else:        myHero.Score_Heart-=5
                    engineBlood.add_obj(h_x-3,h_y-3,random.randrange(0,29,1))
                    engineBlood.add_obj(h_x,h_y,random.randrange(0,29,1))
                    engineBlood.add_obj(h_x+3,h_y+3,random.randrange(0,29,1))
                    sound_alex.sound_pain()
                    ret=1

                if myHero.Score_Heart<0: myHero.Score_Heart=0
                return ret

            
            def show(self,scll):
                global engineLevel
                ScrollX = (engineLevel.engineMaps.MapStartPositionW*32)+engineLevel.engineMaps.MapScrollX
                ScrollY = engineLevel.engineMaps.MapScrollY

                for a in self.ObjArrow:                                
                                a.radius+=1
                                if a.radius>4:
                                    a.angle-=1
                                    a.radius=0
                                    a.power_y+=0.1
                                
                                
                                radian=(a.angle*3.14159/180)
                                x = a.power_x*math.cos(radian)
                                y = a.power_x*math.sin(radian)
                                
                                a.position_x+=x
                                a.position_y+=(y+a.power_y)
                                self.ImageArrow[a.sprite].angle=180+a.angle
                                self.ImageArrow[a.sprite].draw(dstrect=(a.position_x-ScrollX, a.position_y-ScrollY))
                                if self.check_is_hero(self.ImageArrow[a.sprite],a.position_x-ScrollX,a.position_y-ScrollY,a.sprite)==1:
                                    self.ObjArrow.remove(a)
                                    engineLevel.ObjAi[a.index].count-=1
                                    continue

                                if a.position_x-ScrollX<-32 or a.position_x-ScrollX>2000:
                                            self.ObjArrow.remove(a)
                                            engineLevel.ObjAi[a.index].count-=1
                                            continue
                                if a.position_y<-100 or a.position_y>850:
                                            self.ObjArrow.remove(a)
                                            engineLevel.ObjAi[a.index].count-=1
                                            continue

                for m in self.ObjMagic:                    
                                m.w_angle+=1
                                m.radius+=1
                                if m.radius>4:
                                    m.angle-=1                                    
                                    m.power_y+=0.1
                                
                                if m.w_angle>=360: m.w_angle=0
                                radian=(m.angle*3.14159/180)
                                x = m.power_x*math.cos(radian)
                                y = m.power_x*math.sin(radian)
                                
                                m.position_x+=x
                                m.position_y+=(y+m.power_y)
                                self.ImageMag[m.sprite].angle=m.w_angle
                                self.ImageMag[m.sprite].draw(dstrect=(m.position_x-ScrollX-scll, m.position_y-ScrollY))
                                if self.check_is_hero(self.ImageMag[m.sprite],m.position_x-ScrollX,m.position_y-ScrollY,3+m.sprite)==1:
                                        self.ObjMagic.remove(m)
                                        engineLevel.ObjAi[m.index].count-=1
                                        continue


                                if m.sprite==6: #shtorm
                                    if m.radius==30:
                                            for n in range(40):
                                                angle=n*9
                                                self.add_arrow_cycle(m.position_x,m.position_y,0, m.index, angle)
                                                engineLevel.ObjAi[m.index].count+=1                                                
                                            sound_alex.sound_arrow()
                                            self.ObjMagic.remove(m)
                                            engineLevel.ObjAi[m.index].count-=1
                                            continue

                                if m.position_x-ScrollX<-32 or m.position_x-ScrollX>2000:
                                            self.ObjMagic.remove(m)
                                            engineLevel.ObjAi[m.index].count-=1
                                            continue
                                if m.position_y<-100 or m.position_y>850:
                                            self.ObjMagic.remove(m)
                                            engineLevel.ObjAi[m.index].count-=1
                                            continue
            def ai(self): #artificial intelligence
                global engineLevel
                global myHero 
                ScrollX = (engineLevel.engineMaps.MapStartPositionW*32)+engineLevel.engineMaps.MapScrollX
                ScrollY = engineLevel.engineMaps.MapScrollY
                for i in range(engineLevel.engineHeroes.HeroesCount):
                    objs=engineLevel.engineHeroes.myHeroes[i]
                    obj=objs[0]
                    x=objs[1] 
                    y=objs[2]
                    heart=objs[3]
                    state=objs[4]
                    if state>0: continue 

                    if (x-ScrollX)>100 and (x-ScrollX)<1890:
                                     objAi=engineLevel.ObjAi[i]
                                     if engineLevel.ObjAi[i].time>0: engineLevel.ObjAi[i].time-=1
                                     if engineLevel.alpha==255    and   objAi.count<2   and   engineLevel.ObjAi[i].time==0:
                                         
                                         engineLevel.ObjAi[i].count+=1
                                         engineLevel.ObjAi[i].time=self.TimeRepit
                                         spr=random.randrange(0, 5,1)
                                         if obj<3:
                                            self.add_arrow(x-5,y+15,obj, i)
                                            sound_alex.sound_arrow()
                                         if obj>3:
                                            if obj==10:  spr=6
                                            self.add_magic(x-5,y+10,spr, i)
                                            sound_alex.sound_magic()
                    

                



                    


#--------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------


class SpriteSmoke():
        def __init__(self,x,y,angle,direction):
            self.curr_time=0
            self.curr_alpha=255                                  
            self.position_x=x+0.00
            self.position_y=y+0.00
            self.angle=angle
            self.direction=random.randrange(-1, 2)
            self.sprites=0
            self.delay=0
            
class SpriteBlood():
        def __init__(self,x,y,spr):
            self.curr_time=0
            self.curr_alpha=255                                  
            self.position_x=x+0.00
            self.position_y=y+0.00
            self.sprites=spr
            self.power_x=random.randrange(-4, 4, 1)
            self.power_y=random.randrange(0, 2, 1)
            self.delay=0

class SpriteRocket():
        def __init__(self,x,y,angle,direction):
            self.curr_time=0
            self.curr_alpha=255                                  
            self.position_x=x+0.00
            self.position_y=y+0.00
            self.max_x=0
            self.max_y=0
            self.radius=0
            self.angle=angle
            self.direction=direction
            self.engine_smokes=[]
            self.smoke_int=0
            

def rocket_add():
    if myHero.FlipX==0:
        r_x=98
        r_y=32
        angle=360
        radian=(angle*3.14159/180)
        x = r_x*math.cos(radian)
        #x=98
        y = r_y*math.sin(radian)
        add=32+24
        myRockets.add(myHero.position_x+x,myHero.position_y+add,0, myHero.FlipX )
    else:
        r_x=32 
        r_y=32
        angle1=-90  
        radian1=(angle1*3.14159/180) 
        angle2=0  
        radian2=(angle2*3.14159/180) 

        x = r_x*math.cos(radian1)
        #x=98
        y = r_y*math.sin(radian2)
        add=32+24
        myRockets.add(myHero.position_x+32-x,myHero.position_y+add-y,0, myHero.FlipX )

def load_smoke(render, file):
            image = pygame.image.load(utils_alex.zip_arch(file))            
            texture = Texture.from_surface(render, image)
            img=Image(texture, (0,0,texture.width, texture.height))
            img.blend_mode=1
            return img
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class EngineBlood():
        def __init__(self,renderer):
            self.renderer=renderer
            self.image=[]
            self.ObjBlood=[]
            self.ObjBloodMonstr=[]

            for i in range(1,30,1):
                str_name='blood_{:02d}.png'.format(i)
                self.image.append(get_img(renderer,str_name))
        
        def add_obj(self, x,y, obj):
            obj=SpriteBlood(x,y,obj)
            self.ObjBlood.append(obj)

        def add_obj_monstr(self, x,y, obj):
            obj=SpriteBlood(x,y,obj)
            self.ObjBloodMonstr.append(obj)

        def show(self):
            global engineBlood
            global engineLevel
            ScrollX = (engineLevel.engineMaps.MapStartPositionW*32)+engineLevel.engineMaps.MapScrollX;
            ScrollY = engineLevel.engineMaps.MapScrollY
            for b in self.ObjBlood: 
                b.curr_time+=1
                b.position_y+=0.3
                b.curr_alpha-=1
                self.image[b.sprites].alpha=b.curr_alpha
                self.image[b.sprites].draw(dstrect=(b.position_x, b.position_y))
                if b.curr_time>240:
                        self.ObjBlood.remove(b)

            for m in self.ObjBloodMonstr: 
                if m.curr_time<200:
                    m.curr_time+=1
                    m.position_y+=0.3+ (m.power_y/10)  
                    m.position_x+=(m.power_x/10)
                self.image[m.sprites].alpha=255
                self.image[m.sprites].draw(dstrect=(m.position_x-ScrollX, m.position_y-ScrollY))


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------    

class EngineRocket():
        def __init__(self, file, file1, file2,file3, file4, file5, file6, file7,renderer):
            self.renderer=renderer
            image = pygame.image.load(utils_alex.zip_arch(file))
            texture = Texture.from_surface(self.renderer, image)
            texture.blend_mode=1
            self.image=Image(texture, (0,0,texture.width, texture.height))
            self.image.blend_mode=1
            self.rockets=[]
            self.smoke=[]            
            self.smoke.append(load_smoke(renderer,file1))
            self.smoke.append(load_smoke(renderer,file2))
            self.smoke.append(load_smoke(renderer,file3))
            self.smoke.append(load_smoke(renderer,file4))
            self.smoke.append(load_smoke(renderer,file5))
            self.smoke.append(load_smoke(renderer,file6))
            self.smoke.append(load_smoke(renderer,file7))
            


        def add(self, x,y,angle,direction ):
            spriteRocket=SpriteRocket(x,y,angle,direction)
            self.rockets.append(spriteRocket)


        def show(self):
             for r in self.rockets: 
                    self.image.angle=r.angle

                    if r.direction==1:
                        self.image.flip_x=True
                    else:
                        self.image.flip_x=False
                                  
                    if r.direction==0:
                                r.radius+=6 
                                angle=0
                                if r.angle<0:
                                        angle=-r.angle
                                else:
                                        angle=360-r.angle

                                radian=(angle*3.14159/180)
                                x = r.radius*math.cos(radian)
                                y = r.radius*math.sin(radian)
                                r.smoke_int+=1
                                if r.smoke_int>5:
                                    r.smoke_int=0
                                    y_c=32*math.sin(radian)
                                    smoke=SpriteSmoke(r.position_x+x-20, r.position_y-y-9+y_c,r.angle,r.direction)                                    
                                    r.engine_smokes.append(smoke)
                                for s in r.engine_smokes:
                                    s.position_y+=(s.direction/10)
                                    self.smoke[s.sprites].draw(dstrect=(s.position_x, s.position_y))
                                    s.delay+=1
                                    if  s.delay>15:
                                        s.delay=0
                                        s.sprites+=1
                                        if s.sprites>6:
                                            r.engine_smokes.remove(s)
                                            continue
                                
                                self.image.draw(dstrect=(r.position_x+x, r.position_y-y))
                                if r.position_x+x>2000:
                                            self.rockets.remove(r)
                                            continue
                                if r.position_y-y<-100:
                                            self.rockets.remove(r)
                                            continue
                                if r.position_y-y>1000:
                                            self.rockets.remove(r)
                                            continue


                    if r.direction==1:
                                r.radius+=6
                                angle=0
                                if r.angle<0:
                                        angle=-r.angle
                                else:
                                        angle=360-r.angle

                                radian=(angle*3.14159/180)
                                x = r.radius*math.cos(radian)
                                y = r.radius*math.sin(radian)

                                r.smoke_int+=1
                                if r.smoke_int>5:
                                    r.smoke_int=0
                                    y_c=32*math.sin(radian)
                                    smoke=SpriteSmoke(r.position_x-x+20, r.position_y+y-9-y_c,r.angle,r.direction)                                    
                                    r.engine_smokes.append(smoke)
                                for s in r.engine_smokes:
                                    s.position_y+=(s.direction/10)
                                    self.smoke[s.sprites].draw(dstrect=(s.position_x, s.position_y))
                                    s.delay+=1
                                    if  s.delay>15:
                                        s.delay=0
                                        s.sprites+=1
                                        if s.sprites>6:
                                            r.engine_smokes.remove(s)
                                            continue
                                
                                self.image.draw(dstrect=(r.position_x-x, r.position_y+y))
                                if r.position_x-x<-100:
                                            self.rockets.remove(r)
                                            continue
                                if r.position_y+y<-100:
                                            self.rockets.remove(r)
                                            continue
                                if r.position_y+y>1000:
                                            self.rockets.remove(r)
                                            continue


#--------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------

def engine_cartridge(scrll):
        myCartridge.show(scrll)
#-----------------------------------------------------------------------------------------------

def engine_init(renderer, max_x, max_y):
        global mySky
        global myHero
        global myKey_lr
        global myKey_ud
        global myKey_wx
        global myCartridge

        global engineLevel
        global myMagic

        global engineBlood

        myHero=EngineHero(MAN_X,MAN_Y,renderer)
        mySky=EngineImage("sky.png" ,renderer)
        #myRockets=EngineRocket("rocket.png", "smoke1.png","smoke2.png","smoke3.png","smoke4.png","smoke5.png","smoke6.png","smoke7.png",renderer)
        myCartridge=EngineCartridge("shot.png", "arrow.png",  renderer)
        engineBlood= EngineBlood(renderer)
        myMagic=EngineMagic(renderer)

        mySky.curr_alpha=200
        mySky.max_x=max_x # 2000- 1480=520   
        mySky.max_y=max_y #800
        mySky.position_x=0 #2000
        mySky.position_y=-200 #1000-800
        myKey_lr=0
        myKey_ud=0
        myKey_wx=0

        engineLevel=maps_engine.EngineLevel(renderer)

        engineLevel.SetLevel(0)

    
#-----------------------------------------------------------------------------------------------
def engine():
          
         global engineLevel
         alpha=engineLevel.alpha
         engine_sky(alpha)

         scrll=engineLevel.MapShow()
         engineLevel.ObjsShow85_152()  # the background
         engineLevel.HeroesShow()
         engine_cartridge(scrll)   
         engine_hero(scrll)

         engineLevel.ObjsShow00_84() # the foreground

         myMagic.ai()
         myMagic.show(scrll)
                  
         engineBlood.show()

         global myHero
         if myHero.State<11:
            myHero.Score_Monster=engineLevel.monster_count
            myHero.score(engineLevel.current_level, myHero.Score_Heart, myHero.Score_Arrows, myHero.Score_Ammo, myHero.Score_Gun_angle, myHero.Score_Monster, alpha)
        
         if myHero.State==11:
            engineLevel.alphaUp=0
            myHero.complete()
            if engineLevel.alpha==0:
                engineLevel.current_level+=1
                if engineLevel.current_level<10:
                    StartGame(engineLevel.current_level, False)




#-----------------------------------------------------------------------------------------------
def menu_engine():         
         global engineLevel
         alpha=engineLevel.alpha
         engine_sky(alpha)

         scrll=engineLevel.MapShow()
         engineLevel.ObjsShow85_152()  # the background
         engineLevel.ObjsShow00_84() # the foreground

         if engineLevel.engineMaps.MapScrollDirection==0: engineLevel.engineMaps.MapScrollDirection=1
         
         if engineLevel.engineMaps.MapScrollDirection==1:             
            if engineLevel.engineMaps.MapStartPositionW>=150: engineLevel.engineMaps.MapScrollDirection=-1

         if engineLevel.engineMaps.MapScrollDirection==-1:             
            if engineLevel.engineMaps.MapStartPositionW==0: engineLevel.engineMaps.MapScrollDirection=1

         

#-----------------------------------------------------------------------------------------------
#K_DOWN K_UP K_RIGHT K_LEFT 
#
def set_key(key):
    global myKey_lr
    global myKey_ud
    global myKey_wx
    global myHero
    if key==pygame.K_LEFT or key==pygame.K_RIGHT:    
                myKey_lr=key
    if key==pygame.K_UP or key==pygame.K_DOWN:    
                myKey_ud=key   

    if key==pygame.K_LCTRL:
            myHero.Ammo()

    if key==pygame.K_SPACE:
            myHero.Jump()


    if key==pygame.K_q  or key==pygame.K_a:
            myKey_wx=key

    if key==pygame.K_TAB:
            if myHero.current_Gun==0: myHero.current_Gun=1
            else: myHero.current_Gun=0

    if key==pygame.K_ESCAPE:
        global engineLevel
        global game_mode
        game_mode=1
        engineLevel.SetLevel(0)

            

    #myHero.no_change()
#-----------------------------------------------------------------------------------------------
#K_DOWN K_UP K_RIGHT K_LEFT 
#
def clear_key(key): 
    global myKey_lr
    global myKey_ud
    global myKey_wx

    if key==pygame.K_LEFT or key==pygame.K_RIGHT:    
                myKey_lr=0
    if key==pygame.K_UP or key==pygame.K_DOWN:    
                myKey_ud=0
    if key==pygame.K_q or key==pygame.K_a:
                myKey_wx=0     


#-----------------------------------------------------------------------------------------------
def StartGame(level,new_game):
    global engineLevel,game_mode
    global  myMagic
    global  myHero
    
    global engineBlood

    engineLevel.SetLevel(level)
    game_mode=2
    add=level
    if add>50: add=51
    myMagic.TimeRepit=400-add
    myMagic.ObjArrow.clear()
    myMagic.ObjMagic.clear()
    myHero.position_x=MAN_X
    myHero.position_y=MAN_Y
    myHero.Score_Gun_angle=20

    if new_game==True:
        myHero.Score_Arrows=999        
        myHero.Score_Ammo=500
        myHero.Score_Heart=100
    else:
        myHero.Score_Arrows+=150
        myHero.Score_Ammo+=50
        if myHero.Score_Heart<90: myHero.Score_Heart+=10
        else: myHero.Score_Heart=100

    myHero.Score_Monster=0
    myHero.State=0
    #engineLevel

    engineBlood.ObjBlood.clear()
    engineBlood.ObjBloodMonstr.clear()

    #-----------------------------------------------------------------------------------------------
def ExitGame():
    global game_mode
    game_mode=3
    #-----------------------------------------------------------------------------------------------
def SetFPS(fps):
    global FPS
    FPS=fps
    #-----------------------------------------------------------------------------------------------

def colliderect(self, *other):
        rect = self.__class__(*other)
        return (
            self.x < rect.x + rect.w and
            self.y < rect.y + rect.h and
            self.x + self.w > rect.x and
            self.y + self.h > rect.y
        )

def update():
        global clock
        global renderer
        renderer.present()                                
        clock.tick(FPS)
        return clock.get_fps()
        


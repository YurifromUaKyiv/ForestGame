import pygame  
import math
import random
from pygame._sdl2 import Window, Texture, Image, Renderer

import engine_alex
import utils_alex
import numpy

MapBlockSize=32
Tiles_max=516
Obj_max=152
Heroes_max=214
    
DirectionLeft=-1
DirectionRight=1
DirectionUp=-2
DirectionDown=2


def binToUint16(bin, p):    
    uint16=int(bin[p])+ int(bin[p+1]<<8)
    return uint16

def binToUint32(bin, p):    
    int64=int(bin[p])+int(bin[p+1]<<8)+int(bin[p+2]<<16)+int(bin[p+3]<<24)
    if int64 > 0x7fffffff:
        int32= 0x100000000-int64
        int64=-int32


    return int64


class EngineMaps():
        def __init__(self, renderer):
            
            
            self.ImageMap=[]
            self.myMap=[]

            self.MapStartPositionW=0
            self.MapScrollXInc=1
            self.MapScrollYInc=1
            self.MapScrollX=0            
            self.MapScrollY=0
            self.MapScrollDirection=0 # -1 1 -2 2
            self.MapH=0
            self.MapW=0
            
            for i in range(1,Tiles_max,1):
                str_name='Tile_{:03d}.png'.format(i)
                self.ImageMap.append(engine_alex.get_img(renderer,str_name))
            count=len(self.ImageMap)
            

#--------------------------------------------------------------------------

class EngineObjs():
        def __init__(self, renderer):

            self.ImageObj=[]
            self.myObjects=[]
            self.ObjCount=0


            for i in range(1,Obj_max,1):
                str_name='Obj_{:03d}.png'.format(i)
                self.ImageObj.append(engine_alex.get_img(renderer,str_name))
#--------------------------------------------------------------------------

class EngineHeroes():
        def __init__(self, renderer):

            self.ImageHeros=[]
            self.myHeroes=[]
            self.HeroesCount=0
            for i in range(1,Heroes_max,1):
                str_name='Hero_{:03d}.png'.format(i)
                self.ImageHeros.append(engine_alex.img_to_text64(renderer,str_name))
#--------------------------------------------------------------------------
class EngineAI():
        def __init__(self,index):
            self.index=index
            self.magic_count=0
            self.time=random.randrange(0,300,10)
            self.count=0
        
#--------------------------------------------------------------------------

class EngineLevel():
        #--------------------------------------
        def __init__(self, renderer):
            self.engineMaps=EngineMaps(renderer)
            self.engineObjs=EngineObjs(renderer)
            self.engineHeroes=EngineHeroes(renderer)

            self.ImageSkelet=[]
            self.ImageSkelet.append(engine_alex.img_to_text64(renderer,"skeleton01.png"))
            self.ImageSkelet.append(engine_alex.img_to_text64(renderer,"skeleton02.png"))
            self.ImageSkelet.append(engine_alex.img_to_text64(renderer,"skeleton03.png"))
            self.ImageSkelet.append(engine_alex.img_to_text64(renderer,"skeleton04.png"))
            self.ImageSkelet.append(engine_alex.img_to_text64(renderer,"skeleton05.png"))


            self.up1=0            
            self.up1_x=0            
            self.up1_y=0            

            self.up2=0            
            self.up2_x=0            
            self.up2_y=0     

            self.up3=0            
            self.up3_x=0            
            self.up3_y=0            

                        

            self.mid1=0
            self.mid2=0
            self.mid3=0

            self.sh1=0
            self.sh2=0
            self.sh3=0

            self.dw1=0
            self.dw1_x=0
            self.dw1_y=0

            self.dw2=0
            self.dw2_x=0
            self.dw2_y=0

            self.dw3=0
            self.dw3_x=0
            self.dw3_y=0

            self.vsync=0
            self.ObjAi=[]
            self.alpha=0
            self.alphaUp=1

            self.current_level=-1
            
            self.monster_count=0

        #--------------------------------------

        def SetLevel(self, level):
            
            self.current_level=level
            level_name='Level_{:02d}.map'.format(level)
            bin=utils_alex.file_level_read(level_name)
            self.alpha=0
            self.alphaUp=1
            self.ObjAi=[]
            self.engineMaps.myMap=[]
            self.engineMaps.MapStartPositionW=0
            self.engineMaps.MapScrollXInc=1
            self.engineMaps.MapScrollYInc=1
            self.engineMaps.MapScrollX=0            
            self.engineMaps.MapScrollY=0
            self.engineMaps.MapScrollDirection=0 # -1 1 -2 2
            self.engineMaps.MapH=0
            self.engineMaps.MapW=0
            self.engineObjs.myObjects=[]
            self.engineObjs.myObjects.clear()
            self.engineHeroes.myHeroes=[]
            self.engineHeroes.myHeroes.clear()
            
            
            
            #map
            p=0
            if bin[p]!=0xf1 or bin[p+1]!=0x01:          return  
            p+=2
            #H
            self.engineMaps.MapH=binToUint16(bin,p)
            p+=2
            #H
            self.engineMaps.MapW=binToUint16(bin,p)
            p+=2            
            self.engineMaps.myMap.clear()
            for w in range(self.engineMaps.MapW):
                for h in range(self.engineMaps.MapH):
                    self.engineMaps.myMap.append(binToUint16(bin,p))
                    p+=3 #1Reserved            
           
            print('Level W:', self.engineMaps.MapW, 'Level Size:', len(self.engineMaps.myMap) )

            #Obj
            if bin[p]!=0xf2 or bin[p+1]!=0x01:          return
            p+=2
            self.engineObjs.ObjCount=binToUint16(bin,p)
            p+=2
            for i in range(self.engineObjs.ObjCount):
                obj=binToUint16(bin,p)
                p+=2
                x=binToUint32(bin,p)
                p+=4
                y=binToUint32(bin,p)
                p+=4
                objs=[]
                objs.append(obj)
                objs.append(x)
                objs.append(y)
                self.engineObjs.myObjects.append(objs)


            self.ObjAi=[]
            self.ObjAi.clear()
            #Heroes
            if bin[p]!=0xf3 or bin[p+1]!=0x01:          return
            p+=2
            self.engineHeroes.HeroesCount=binToUint16(bin,p)
            p+=2
            for i in range(self.engineHeroes.HeroesCount):
                obj=binToUint16(bin,p)
                p+=2
                x=binToUint32(bin,p)
                p+=4
                y=binToUint32(bin,p)
                p+=4
                objs=[]
                objs.append(obj)
                objs.append(x)
                objs.append(y)
                heart=50
                state=0
                objs.append(heart)
                objs.append(state)

                self.engineHeroes.myHeroes.append(objs)
                self.ObjAi.append(EngineAI(i))

        def MapGetObjs(self, x,y,w,h,scroll):
                log=0
                start_index = self.engineMaps.MapH * self.engineMaps.MapStartPositionW;
                #//up1
                pos_x_u1=int((x+2+self.engineMaps.MapScrollX)/MapBlockSize)
                pos_y_u1=int((y-24)/MapBlockSize)
                                           
                pos=(pos_x_u1*self.engineMaps.MapH)+24-pos_y_u1
                m=self.engineMaps.myMap[start_index+pos]                
                if m!=self.up1: 
                    log=1
                self.up1=m
                self.up1_x=(pos_x_u1*32)
                self.up1_y=(pos_y_u1)*32
                
                m=self.engineMaps.myMap[start_index+pos+25] #next row                
                if m!=self.up2: 
                    log=1

                self.up2=m
                self.up2_x=self.up1_x+32
                self.up2_y=self.up1_y

                m=self.engineMaps.myMap[start_index+pos+25+25]                
                if m!=self.up3: 
                    log=1

                self.up3=m
                self.up3_x=self.up1_x+32+32
                self.up3_y=self.up1_y

                m=self.engineMaps.myMap[start_index+pos-1]                
                if m!=self.mid1: 
                    log=1
                self.mid1=m                

                m=self.engineMaps.myMap[start_index+pos-1+25]                
                if m!=self.mid2: 
                    log=1
                self.mid2=m

                m=self.engineMaps.myMap[start_index+pos-1+25+25]                
                if m!=self.mid3: 
                    log=1
                self.mid3=m

                m=self.engineMaps.myMap[start_index+pos-2]                
                if m!=self.sh1: 
                    log=1
                self.sh1=m                

                m=self.engineMaps.myMap[start_index+pos-2+25]                
                if m!=self.sh2: 
                    log=1
                self.sh2=m

                m=self.engineMaps.myMap[start_index+pos-2+25+25]                
                if m!=self.sh3: 
                    log=1
                self.sh3=m

                m=self.engineMaps.myMap[start_index+pos-3]
                if m!=self.dw1: 
                    log=1
                self.dw1=m
                self.dw1_x=self.up1_x
                self.dw1_y=self.up1_y+96

                m=self.engineMaps.myMap[start_index+pos-3+25]
                if m!=self.dw2: 
                    log=1
                self.dw2=m
                self.dw2_x=self.up1_x+32
                self.dw2_y=self.dw1_y

                m=self.engineMaps.myMap[start_index+pos-3+25+25]
                if m!=self.dw3: 
                    log=1
                self.dw3=m
                self.dw3_x=self.up1_x+32+32
                self.dw3_y=self.dw1_y

                if log==1:
                    print ('New Map:', self.up1,'<>', self.up2, '<>', self.up3, '    ', self.mid1,'<>', self.mid2, '<>', self.mid3,' ',self.sh1,'<>', self.sh2, '<>', self.sh3,' ', self.dw1,'<>', self.dw2, '<>', self.dw3)


        #--------------------------------------
        def MapScrollingAnalyze(self, x,y):
            #0-1900
            x=int(x/190)
            ret=0
            if   x==0:
                self.engineMaps.MapScrollDirection=-1
                self.engineMaps.MapScrollXInc=32                
            elif x==1:
                self.engineMaps.MapScrollDirection=-1
                self.engineMaps.MapScrollXInc=16
            elif x==2:
                self.engineMaps.MapScrollDirection=-1
                self.engineMaps.MapScrollXInc=8
            elif x==3:
                self.engineMaps.MapScrollDirection=-1
                self.engineMaps.MapScrollXInc=4
            elif x==4:
                self.engineMaps.MapScrollDirection=-1
                self.engineMaps.MapScrollXInc=2

            elif x==5:
                self.engineMaps.MapScrollDirection=0
                self.engineMaps.MapScrollXInc=0

            elif x==6:
                self.engineMaps.MapScrollDirection=1
                self.engineMaps.MapScrollXInc=2
            elif x==7:
                self.engineMaps.MapScrollDirection=1
                self.engineMaps.MapScrollXInc=4
            elif x==8:
                self.engineMaps.MapScrollDirection=1
                self.engineMaps.MapScrollXInc=8
            elif x==9:
                self.engineMaps.MapScrollDirection=1
                self.engineMaps.MapScrollXInc=16
            elif x==10:
                self.engineMaps.MapScrollDirection=1
                self.engineMaps.MapScrollXInc=32
            


        def MapShow(self):
            
            scrll=0
            self.vsync+=1
            if self.vsync>=10:
                        self.vsync=0

            if self.engineMaps.MapScrollDirection==1 and self.engineMaps.MapStartPositionW < self.engineMaps.MapW-100: #DirectionLeft
                self.engineMaps.MapScrollX+=self.engineMaps.MapScrollXInc
                scrll=self.engineMaps.MapScrollXInc
                if self.engineMaps.MapScrollX>=32:
                    if self.engineMaps.MapStartPositionW < self.engineMaps.MapW-60:
                        self.engineMaps.MapStartPositionW+=1
                        self.engineMaps.MapScrollX=0
                        #if  self.engineMaps.MapStartPositionW>5:       self.engineMaps.MapScrollDirection=-1
                    else: scrll=self.engineMaps.MapScrollXInc


            if self.engineMaps.MapScrollDirection==-1 and self.engineMaps.MapStartPositionW > 0: #DirectionRight
                self.engineMaps.MapScrollX-=self.engineMaps.MapScrollXInc
                scrll=-self.engineMaps.MapScrollXInc
                if self.engineMaps.MapScrollX <= 0:
                    if self.engineMaps.MapStartPositionW > 0:
                        self.engineMaps.MapStartPositionW-=1
                        self.engineMaps.MapScrollX=32
                    else: scrll=0
                #if  self.engineMaps.MapStartPositionW==0:               self.engineMaps.MapScrollDirection=1


            if self.alphaUp==1:
                if self.alpha<255: self.alpha+=1
            else:
                if self.alpha>0: self.alpha-=1

            start_index = self.engineMaps.MapH * self.engineMaps.MapStartPositionW;
            lenMap=len(self.engineMaps.myMap)
            for w in range(61):
                for h in range(self.engineMaps.MapH):
                    num_image=self.engineMaps.myMap[start_index]
                    if self.vsync==0:                        
                        if num_image==54: self.engineMaps.myMap[start_index]=55
                        if num_image==55: self.engineMaps.myMap[start_index]=54
                        if num_image==198: self.engineMaps.myMap[start_index]=199
                        if num_image==199: self.engineMaps.myMap[start_index]=198
                        if num_image==190: self.engineMaps.myMap[start_index]=191
                        if num_image==191: self.engineMaps.myMap[start_index]=190
                        if num_image==211: self.engineMaps.myMap[start_index]=214
                        if num_image==214: self.engineMaps.myMap[start_index]=211
                        if num_image==212: self.engineMaps.myMap[start_index]=213
                        if num_image==213: self.engineMaps.myMap[start_index]=212
                        if num_image==216: self.engineMaps.myMap[start_index]=217
                        if num_image==217: self.engineMaps.myMap[start_index]=218
                        if num_image==218: self.engineMaps.myMap[start_index]=220
                        if num_image==220: self.engineMaps.myMap[start_index]=221
                        if num_image==221: self.engineMaps.myMap[start_index]=223
                        if num_image==223: self.engineMaps.myMap[start_index]=216
                        
                        if num_image==225: self.engineMaps.myMap[start_index]=226
                        if num_image==226: self.engineMaps.myMap[start_index]=225

                        if num_image==228: self.engineMaps.myMap[start_index]=229
                        if num_image==229: self.engineMaps.myMap[start_index]=231
                        if num_image==231: self.engineMaps.myMap[start_index]=228

                        if num_image==314: self.engineMaps.myMap[start_index]=315
                        if num_image==315: self.engineMaps.myMap[start_index]=316
                        if num_image==316: self.engineMaps.myMap[start_index]=317
                        if num_image==317: self.engineMaps.myMap[start_index]=314


                    if num_image>0:
                        x=(w*32)-self.engineMaps.MapScrollX
                        y=(800-32)-(h*32)-self.engineMaps.MapScrollY
                        self.engineMaps.ImageMap[num_image-1].alpha=self.alpha
                        self.engineMaps.ImageMap[num_image-1].draw(dstrect=(x, y))
                    
                    start_index+=1
                    if(start_index>=lenMap): return scrll
            return scrll
        #--------------------------------------
        def ObjsShow00_84(self):
            ScrollX = (self.engineMaps.MapStartPositionW*32)+self.engineMaps.MapScrollX;
            ScrollY = self.engineMaps.MapScrollY
            for i in range(self.engineObjs.ObjCount):                
                objs=self.engineObjs.myObjects[i]
                obj=objs[0]
                if obj<85 or obj==96:
                    x=objs[1] - ScrollX
                    y=objs[2] - ScrollY
                    if x<2000:
                        self.engineObjs.ImageObj[obj].alpha=self.alpha
                        self.engineObjs.ImageObj[obj].draw(dstrect=(x, y))

        def ObjsShow85_152(self):
            ScrollX = (self.engineMaps.MapStartPositionW*32)+self.engineMaps.MapScrollX;
            ScrollY = self.engineMaps.MapScrollY
            for i in range(self.engineObjs.ObjCount):                
                objs=self.engineObjs.myObjects[i]
                obj=objs[0]
                if obj>84 and obj!=96 :
                    x=objs[1] - ScrollX
                    y=objs[2] - ScrollY
                    if x<2000:
                        self.engineObjs.ImageObj[obj].alpha=self.alpha
                        self.engineObjs.ImageObj[obj].draw(dstrect=(x, y))

        #--------------------------------------
        def HeroesShow(self):
            her_count=0
            ScrollX = (self.engineMaps.MapStartPositionW*32)+self.engineMaps.MapScrollX;
            ScrollY = self.engineMaps.MapScrollY
            for i in range(self.engineHeroes.HeroesCount):
                objs=self.engineHeroes.myHeroes[i]
                obj=objs[0]
                x=objs[1] - ScrollX
                y=objs[2] - ScrollY
                heart=objs[3]
                state=objs[4]


                if state==0:
                    self.engineHeroes.ImageHeros[obj].alpha=self.alpha
                    self.engineHeroes.ImageHeros[obj].draw(dstrect=(x, y))
                    her_count+=1

                if state>0:
                    self.ImageSkelet[state-1].alpha=self.alpha
                    self.ImageSkelet[state-1].draw(dstrect=(x, y))
            self.monster_count=her_count

        #--------------------------------------
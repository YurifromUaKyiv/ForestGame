import pygame  
import math
import random
from pygame import mixer
import utils_alex


def mixer_init():
    pygame.mixer.init(frequency=44100)

def muzic_play():
    global mm    
    mm=mixer.Sound(utils_alex.zip_arch("epic_dramatic.mp3"))
    mm.set_volume(0.1)
    mm.play(loops=100)
    

def muzic_stop():
    global mm    
    mm.stop()

def sound_shot1():    
    sss=mixer.Sound(utils_alex.zip_arch("shot1.mp3"))
    sss.set_volume(0.5)
    sss.play()

def sound_ammo_null():
    global ss
    ss=mixer.Sound(utils_alex.zip_arch("ammo_null.mp3"))
    ss.set_volume(0.5)
    ss.play()



def sound_shot2():
    global ss
    ss=mixer.Sound(utils_alex.zip_arch("shot2.mp3"))
    ss.set_volume(0.5)
    ss.play()


def sound_jump():
    global jj
    jj=mixer.Sound(utils_alex.zip_arch("jump.wav"))
    jj.set_volume(0.5)
    jj.play()


def sound_magic():
    global mm
    mm=mixer.Sound(utils_alex.zip_arch("magik.mp3"))
    mm.set_volume(0.5)
    mm.play()

def sound_arrow():
    global aa
    aa=mixer.Sound(utils_alex.zip_arch("arrow.mp3"))
    aa.set_volume(0.5)
    aa.play()

def sound_pain():
    global pp
    pp=mixer.Sound(utils_alex.zip_arch("pain.mp3"))
    pp.set_volume(0.6)
    pp.play()

def sound_pain_monstr():
    global pp1
    pp1=mixer.Sound(utils_alex.zip_arch("pain_m.wav"))
    pp1.set_volume(0.6)
    pp1.play()

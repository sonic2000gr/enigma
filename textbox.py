#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# pygame TextBox sample
#

import pygame
from pygame.locals import *
from sys import exit
import math
from string import uppercase

class TextBox(object):
    def __init__ (self, x,y, width, height, back_color, text_color, text="",centered = False, bordered = False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = (x,y, width, height)
        self.back_color = back_color
        self.text_color = text_color
        self.centered = centered
        self.bordered = bordered
        self.text = text
        self.textfont = pygame.font.SysFont("Verdana", 18, True)
        self.thetext = self.textfont.render(self.text, True, self.text_color, self.back_color)
        
    def getXY(self):
        return (self.x, self.y)

    def setText(self, text):
        self.text = text
        self.thetext = self.textfont.render(self.text, True, self.text_color, self.back_color)

    def clearText(self):
        self.text = ""
        self.thetext = self.textfont.render(self.text, True, self.text_color, self.back_color)

    def getRect(self):
        therect = (self.x, self.y, self.width, self.height)
        return therect

    def getRectWidth(self):
        return self.width

    def getTextWidth(self):
        return self.thetext.get_width()

    def getClicked(self):
        (x,y) = pygame.mouse.get_pos()
        mouserect = Rect(x,y,5,5)
        return mouserect.colliderect(self.getRect())

    def Show(self, surface):
        pygame.draw.rect(surface,self.back_color, self.rect)
        if self.bordered:
            pygame.draw.rect(surface, (0,0,0), self.rect, 2)
            
        y = self.y + (self.height - self.thetext.get_height())/2

        if self.centered:
            x = self.x + (self.width - self.thetext.get_width())/2
        else:
            x = self.x

        surface.blit(self.thetext,(x, y))

def main():

    swidth, sheight = 640,200

    # Initialize pygame library
    
    pygame.init()

    # Initialize the pygame window

    surfacecolor = (50,80,250)
    screen = pygame.display.set_mode((swidth, sheight), DOUBLEBUF, 32)
    pygame.display.set_caption("TextBox Sample App")

    # Create objects
    
    inputbox = TextBox(0, sheight - 80, swidth-10, 40, (255,0,0), (255,255,255)," Input: ")
    outputbox = TextBox(0, sheight - 40, swidth-10, 40, (0,255,0), (255,255,255)," Output: ")  
    button1 = TextBox(280, 50, 100,30, (255,255,0), (0,0,255), "Clear", bordered = True, centered = True)
    
    framerate = 50
    clock = pygame.time.Clock()
    endprogram = False
    cleartext=[]
    cipher=[]
    while not endprogram:

        for event in pygame.event.get():
          if event.type == QUIT:
              endprogram = True
              
          if event.type == KEYDOWN:
              keyboardinput = event.key
              if keyboardinput >=97 and keyboardinput<=122:
                character = chr(keyboardinput - 32)
                cleartext.append(character)
                inputbox.setText(" Input: "+''.join(cleartext))
                cipher.append(chr(ord(character)+1))
                outputbox.setText(" Output: "+''.join(cipher))
                
          if event.type == MOUSEBUTTONDOWN:
                if button1.getClicked():
                  cleartext = []
                  cipher = []
                  inputbox.setText(" Input: ")
                  outputbox.setText(" Output: ")
                

        # fill screen with bluish tint

        screen.fill(surfacecolor)
        inputbox.Show(screen)
        outputbox.Show(screen)
        button1.Show(screen)
            
        time = clock.tick(framerate)
        pygame.display.update()

    # shutdown pygame and exit program
    
    pygame.quit()
    exit()

# Start program
if __name__ == "__main__":
    main()


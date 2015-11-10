#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# pygame graphic rotor sample
#

import pygame
from pygame.locals import *
from sys import exit
import math
from string import uppercase

class Rotor(object):
    def __init__(self, x,y, rotor_radius, startposition,placement, ring_setting,
                 rotor_color=(255,255,0), ring_color=(100,80,250),
                 axle_color=(50,80,250), letter_color_rotor=(0,0,255),
                 letter_color_ring=(255,255,255)):

       #
       # Graphic part initialization
       # Needed by the pygame part
       #
       
       self.x = x
       self.y = y
       self.rotor_radius = rotor_radius
       if self.rotor_radius < 100:
           self.rotor_radius = 100
       self.ring_radius = self.rotor_radius - 40
       self.axle_radius = self.rotor_radius - 80
       self.letter_color_rotor = letter_color_rotor
       self.letter_color_ring = letter_color_ring
       self.rotor_color = rotor_color
       self.ring_color = ring_color
       self.axle_color = axle_color
       self.letter_background_rotor = self.rotor_color
       self.letter_background_ring = self.ring_color
       self.correction_factor = float(pygame.display.Info().current_w) / pygame.display.Info().current_h
       self.angle_step = 360.0 / 26.0
       self.forward_cipher_highlight = []
       self.reverse_cipher_highlight = []

       # Not meant to be used by itself, subclass this
       # for the type of rotors you need.
       # A connections list is needed for this to work

       self.ring_setting = ring_setting
       self.letter_ring = [ chr(i) for i in range(65,91)]

       self.rotateRings()      
       
       self.placement = placement
       
       # Get a number from letter, ie 'A' = 65 - 65 = 0, B = 66-65 = 1 etc.
       
       self.position = 0
       
       # Rotate rotor to starting position
       
       for i in range(0, ord(startposition)-65):
         self.rotate()

    def rotateRings(self):
       self.adjusted_letter = list(self.letter_ring)
       self.adjusted_letter = self.adjusted_letter[self.ring_setting-1:] + self.adjusted_letter[0:self.ring_setting-1]  
       self.adjusted_connections = []
       for i in self.connections:
         neword = ord(i)+ self.ring_setting - 1
         if neword > 90:
             neword = neword - 26
         self.adjusted_connections.append(chr(neword))
       self.forward_cipher = dict(zip(self.adjusted_letter, self.adjusted_connections))
       self.reverse_cipher = dict(zip(self.adjusted_connections, self.adjusted_letter))


    def increaseRingSetting(self):
        self.ring_setting += 1
        if self.ring_setting > 26:
            self.ring_setting = 1
        self.rotateRings()

    def getRingSetting(self):
        return self.ring_setting

    def rotate(self):
        self.position +=1
        if self.position > 25:
            self.position = 0
       
        # Rotate visible letter window, one position at a time
        # just like the real thing (slow!!!)
       
        self.letter_ring = self.letter_ring[1:] + self.letter_ring[0:1]

    def cipher(self, input_pin):
        
        # Rotate before ciphering
        # if rotor is used in rightmost position (placement == Right)
        
        if self.placement == 'Right':
            self.rotate()

        # Get the actual letter
        
        inputletter = self.letter_ring[input_pin]

        # Perform forward cipher
        
        outputletter = self.forward_cipher[inputletter]

        # Get output position, again from ring
        
        output_pin = self.letter_ring.index(outputletter)

        # Save the pins to a list
        # for rotor.show to highlight them during the screen update
        
        self.forward_cipher_highlight = [input_pin, output_pin]
        ext_coordinates = self.getExternalLetterCoordinates(input_pin)
        int_coordinates = self.getInternalLetterCoordinates(output_pin)

        # Return internal/external letter coordinates to the caller
        # The RotorAssembly saves them to a list and draws lines
        # between rotors during its show() function call
        
        return (inputletter, outputletter, output_pin, (ext_coordinates, int_coordinates))

    def reflectCipher(self, input_pin):
        inputletter = self.letter_ring[input_pin]
        outputletter = self.reverse_cipher[inputletter]
        output_pin = self.letter_ring.index(outputletter)

        # Save the pins to a list
        # for rotor.show to highlight them during the screen update

        self.reverse_cipher_highlight = [output_pin, input_pin]

        # Return internal/external letter coordinates to the caller
        # The RotorAssembly saves them to a list and draws lines
        # between rotors during its show() function call
        
        ext_coordinates = self.getExternalLetterCoordinates(output_pin)
        int_coordinates = self.getInternalLetterCoordinates(input_pin)
        return (inputletter, outputletter, output_pin, (int_coordinates, ext_coordinates))

    def justBeforeNotch(self):
        if self.letter_ring[0] == chr(ord(self.notch)-1):
            return True
        else:
            return False

    def reachedNotch(self):
        if self.letter_ring[0] == self.notch:
            return True
        else:
            return False

    def getPosition(self):
        return self.letter_ring[0]
    

    def Show(self, surface, forward_letter_color=(255,0,0), reverse_letter_color=(0,255,0)):

        # Draw the circles that comprise the complete rotor
        
        pygame.draw.circle(surface, self.rotor_color, (self.x, self.y), self.rotor_radius)
        pygame.draw.circle(surface, self.ring_color, (self.x, self.y), self.ring_radius)
        pygame.draw.circle(surface, self.axle_color, (self.x, self.y), self.axle_radius)

        # Print the letters on the external/internal ring, taking self.position
        # into account
        
        self.drawLetters(surface)

        # Check and perform any letter highlights using the lists
        # manipulated by cipher / reflectCipher functions
        
        if self.forward_cipher_highlight:
            self.highlightLetters(surface, self.forward_cipher_highlight, forward_letter_color)
        if self.reverse_cipher_highlight:
            self.highlightLetters(surface, self.reverse_cipher_highlight, reverse_letter_color)

    def drawLetters(self, surface):
        for position in range(0,26):
            self.printExternalLetter(surface, position, self.letter_color_rotor)
            self.printInternalLetter(surface, position, self.letter_color_ring)
           
    def getInternalLetterCoordinates(self, position):

        # Calculate and return the coordinates of a specific letter
        # according to position (internal ring)
        
        angle = -90 + self.angle_step * position
        x = self.ring_radius*math.cos((math.pi*angle)/180.0) + self.x
        y = self.ring_radius*math.sin((math.pi*angle)/180.0) + self.y
        return (x,y)

    def getExternalLetterCoordinates(self, position):

        # Calculate and return the coordinates of a specific letter
        # according to position (external ring)
        
        angle = -90 + self.angle_step * position
        x = self.rotor_radius*math.cos((math.pi*angle)/180.0) + self.x
        y = self.rotor_radius*math.sin((math.pi*angle)/180.0) + self.y
        return (x,y)

    def highlightLetters(self, surface, positions, color):
        self.printExternalLetter(surface, positions[0], color)
        self.printInternalLetter(surface, positions[1], color)

    def resetHighlights(self):
        self.forward_cipher_highlight = []
        self.reverse_cipher_highlight = []
        
    def printInternalLetter(self, surface, position, color=(255,0,0)):

        # Print a letter on the internal ring, on specified position
        # Letter is calculated according to the position requested and
        # current rotor position (self.position)
        
        textfont = pygame.font.SysFont("Courier New",16, True)
        angle =  -90 + self.angle_step * position
        letter = 65 + position + self.position
        if letter > 90:
            letter = letter - 26
        thetext = textfont.render(chr(letter), True, color, self.letter_background_ring)
        offset_x = thetext.get_width()/2.0 + 6 * self.correction_factor
        offset_y = thetext.get_height()/2.0 + 6
        x = (self.ring_radius-offset_x)*math.cos((math.pi*angle)/180.0) + self.x - 5.0
        y = (self.ring_radius-offset_y)*math.sin((math.pi*angle)/180.0) + self.y - (5.0 * self.correction_factor)
        surface.blit(thetext, (x,y))
        
    def printExternalLetter(self, surface, position, color=(255,0,0)):

        # Print a letter on the external ring, on specified position
        # Letter is calculated according to the position requested and
        # current rotor position (self.position)
        
        textfont = pygame.font.SysFont("Courier New",18, True)
        angle =  -90 + self.angle_step * position 
        letter = 65 + position + self.position
        if letter > 90:
            letter = letter - 26
        thetext = textfont.render(chr(letter), True, color, self.letter_background_rotor)
        offset_x = thetext.get_width()/2.0 + 6 * self.correction_factor
        offset_y = thetext.get_height()/2.0 + 6
        x = (self.rotor_radius-offset_x)*math.cos((math.pi*angle)/180.0) + self.x - 5.0
        y = (self.rotor_radius-offset_y)*math.sin((math.pi*angle)/180.0) + self.y - (5.0 * self.correction_factor)
        surface.blit(thetext, (x,y))

class RotorIII(Rotor):
    def __init__(self, x,y, rotor_radius, startposition,placement='Right',
                 ring_setting=1):
        self.connections  = ['B','D','F','H','J','L','C',
                             'P','R','T','X','V','Z','N',
                             'Y','E','I','W','G','A','K',
                             'M','U','S','Q','O']

        self.notch = 'W'
        super(RotorIII,self).__init__(x,y,rotor_radius, startposition,placement, ring_setting)

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

    swidth, sheight = 640,400

    # Initialize pygame library
    
    pygame.init()

    # Initialize the pygame window

    surfacecolor = (50,80,250)
    screen = pygame.display.set_mode((swidth, sheight), DOUBLEBUF, 32)
    pygame.display.set_caption("Graphic Rotor Sample App")

    # Create objects
    
    inputbox = TextBox(0, sheight - 80, swidth-10, 40, (255,0,0), (255,255,255)," Input: ")
    outputbox = TextBox(0, sheight - 40, swidth-10, 40, (0,255,0), (255,255,255)," Output: ")  
    button1 = TextBox(530, 20, 100,30, (255,255,0), (0,0,255), "Clear", bordered = True, centered = True)
    rotor1 = RotorIII(320,140,120,'A','Right',1)
    
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
                theinput = keyboardinput - 32
                character = chr(theinput)
                (inputletter, outputletter, output_pin, (ext_coordinates, int_coordinates))=rotor1.cipher(theinput-65)
                cleartext.append(character)
                inputbox.setText(" Input: "+''.join(cleartext))
                cipher.append(outputletter)
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
        rotor1.Show(screen)
        time = clock.tick(framerate)
        pygame.display.update()

    # shutdown pygame and exit program
    
    pygame.quit()
    exit()

# Start program
if __name__ == "__main__":
    main()


#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# pygame Enigma Simulator
#

import pygame
from pygame.locals import *
from sys import exit
import math
from string import uppercase

swidth,sheight = 1024,400

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
    

    def show(self, surface, forward_letter_color=(255,0,0), reverse_letter_color=(0,255,0)):

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


class Reflector(Rotor):
    def __init__(self, x,y, rotor_radius, startposition,placement, ring_setting,
                 reflector_type='B', rotor_color=(255,255,0), ring_color=(100,80,250),
                 axle_color=(50,80,250), letter_color_rotor=(0,0,255),
                 letter_color_ring=(255,255,255)):
    
        self.setType(reflector_type)


        self.position = 0

        # Pygame specific initialization

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
        self.angle_step = 360 / 26.0
        self.forward_cipher_highlight = []
        self.reverse_cipher_highlight = []

        # End of pygame specific initialization
        
        
    def reflect(self, position):
        if position >=0 and position <=25:
            reflection = self.reflection_table[position]

            # Save highlighted letter to a list
            # to be used during reflector.show() call
            
            self.forward_cipher_highlight = [ position, reflection]
 
            # Return internal/external letter coordinates to the caller
            # The RotorAssembly saves them to a list and draws lines
            # between rotors during its show() function call
            
            ext_coordinates = self.getExternalLetterCoordinates(position)
            int_coordinates = self.getInternalLetterCoordinates(reflection)
            return (reflection, (ext_coordinates, int_coordinates))

    def setType(self, reflector_type):
        self.type = reflector_type
        if self.type !='B' and self.type!='C':
            self.type = 'B'
            
        if self.type == 'B':
            self.reflection_table = [24, 17, 20, 7, 16, 18, 11,
                                      3, 15, 23, 13, 6, 14, 10,
                                     12, 8, 4, 1, 5, 25, 2, 22,
                                     21, 9, 0, 19]
        else:
            self.reflection_table = [5, 21, 15, 9,  8,  0, 14, 24,
                                     4, 3,  17, 25, 23, 13, 6, 2,
                                     19, 10, 20, 16, 18, 1,
                                     13, 12, 7, 11]


    def getType(self):
        return self.type
    

    def rotateRings(self):
        
        # Reflector rings do not rotate :)
        
        return

    def rotate(self):

        # Reflector is a stationary 'rotor' :)
        
        return

    def cipher(self, position):

        # This is equivalent to reflect()
        
        return self.reflect(self, position)

    def reflectCipher(self, position):

        # This is also equivalent to reflect()
        
        return self.reflect(self, position)

    def justBeforeNotch(self):

        # Reflector has no notch; it's stationary
        
        return False

    def reachedNotch(self):

        # See above :)
        
        return False

    def getPosition(self):

        # Reflector does not rotate, position is always 0.
        
        return self.position

class RotorIII(Rotor):
    def __init__(self, x,y, rotor_radius, startposition,placement='Right',
                 ring_setting=1):
        self.connections  = ['B','D','F','H','J','L','C',
                             'P','R','T','X','V','Z','N',
                             'Y','E','I','W','G','A','K',
                             'M','U','S','Q','O']

        self.notch = 'W'
        super(RotorIII,self).__init__(x,y,rotor_radius, startposition,placement, ring_setting)

class RotorII(Rotor):
    def __init__(self,x,y, rotor_radius, startposition,placement='Middle', ring_setting=1):
        self.connections = ['A', 'J', 'D', 'K', 'S', 'I', 'R', 'U',
                            'X', 'B', 'L', 'H', 'W', 'T', 'M', 'C',
                            'Q', 'G', 'Z', 'N', 'P', 'Y', 'F', 'V',
                            'O', 'E' ]
        self.notch = 'F'
        super(RotorII,self).__init__(x,y, rotor_radius, startposition,placement, ring_setting)


class RotorI(Rotor):
    def __init__(self, x,y, rotor_radius, startposition,placement='Left', ring_setting=1):
        self.connections  = [ 'E', 'K', 'M', 'F', 'L', 'G', 'D', 'Q',
                              'V', 'Z', 'N', 'T', 'O', 'W', 'Y', 'H',
                              'X', 'U', 'S', 'P', 'A', 'I', 'B', 'R',
                              'C', 'J' ]
        self.notch = 'R'
        super(RotorI,self).__init__(x,y, rotor_radius, startposition,placement, ring_setting)


class RotorAssembly(object):
    def __init__(self, startposition_left='Α', startposition_middle='Α', startposition_right='Α', reflectortype='B',
                 ring_setting_l=1, ring_setting_m=1, ring_setting_r=1,
                 rotor_x =140, rotor_y=168, rotor_radius = 120):
        rotor_spacing = 2* rotor_radius +5
        self.reflector = Reflector(rotor_x, rotor_y, rotor_radius, 0, 'Left', 0, reflectortype)
        self.rotor_l = RotorI(rotor_x + rotor_spacing, rotor_y, rotor_radius, startposition_left, 'Left',ring_setting_l)
        self.rotor_m = RotorII(rotor_x + rotor_spacing*2, rotor_y, rotor_radius, startposition_middle, 'Middle',ring_setting_m)
        self.rotor_r = RotorIII(rotor_x +rotor_spacing*3, rotor_y, rotor_radius, startposition_right, 'Right',ring_setting_r)
        self.drawing_list =[]

    def reset(self, startposition_left, startposition_middle, startposition_right,
              reflector_type, ring_setting_l, ring_setting_m, ring_setting_r):
        self.reflector.setType(reflector_type)
        
        

    def resetHighlightsAndDrawings(self):
        self.rotor_r.resetHighlights()
        self.rotor_m.resetHighlights()
        self.rotor_l.resetHighlights()
        self.reflector.resetHighlights()
        self.drawing_list = []

    def cipher(self, themessage, showoutput=False):
        if showoutput:
            print "Machine Reset!"
            print "Initial Rotor Positions: " + self.rotor_l.getPosition()+" - "+self.rotor_m.getPosition() +" - " + self.rotor_r.getPosition()
            print "Ring setting: "+ str(self.rotor_l.ring_setting) +" - "+ str(self.rotor_m.ring_setting) +" - "+ str(self.rotor_r.ring_setting)
            print
            print "Simulation running..."
            print
            print "III\tIn\tOut\tPos\tII\tIn\tOut\tPos\tI\tIn\tOut\tPos\tR1-In\tR1-Out\tR1-Pos\tR2-in\tR2-out\tR2-Pos\tR3-In\tR3-Out\tR3-Pos\tC Note"
            print 180*"="
        self.drawing_list = []
        crypto = []
        for letter in themessage:
            if self.rotor_m.justBeforeNotch():
                self.rotor_m.rotate()
                self.rotor_l.rotate()
                justrotated=True
                if showoutput:
                    print "DS"
            else:
                justrotated=False
                if showoutput:
                    print

            (inputletter, outputletter, outpos, coord_r) = self.rotor_r.cipher(ord(letter)-65)
            self.drawing_list.append(coord_r[0])
            self.drawing_list.append(coord_r[1])
            
            if showoutput:
                print self.rotor_r.getPosition()+"\t"+inputletter+"\t"+outputletter+"\t"+str(outpos)+"\t",

            if self.rotor_r.reachedNotch() and not justrotated:
                self.rotor_m.rotate()

            (inputletter, outputletter, outpos, coord_m) = self.rotor_m.cipher(outpos)
            self.drawing_list.append(coord_m[0])
            self.drawing_list.append(coord_m[1])
            if showoutput:
                print self.rotor_m.getPosition()+"\t"+inputletter+"\t"+outputletter+"\t"+str(outpos)+"\t",

            (inputletter, outputletter, outpos, coord_l) = self.rotor_l.cipher(outpos)
            self.drawing_list.append(coord_l[0])
            self.drawing_list.append(coord_l[1])
            if showoutput:
                print self.rotor_l.getPosition()+"\t"+inputletter+"\t"+outputletter+"\t"+str(outpos)+"\t",
                
            (outpos_reflector, coord_reflector) = self.reflector.reflect(outpos)
            self.drawing_list.append(coord_reflector[0])
            self.drawing_list.append(coord_reflector[1])
                                     
            (inputletter, outputletter, outpos, coord_lr) = self.rotor_l.reflectCipher(outpos_reflector)
            self.drawing_list.append(coord_lr[0])
            self.drawing_list.append(coord_lr[1])
            if showoutput:
                print inputletter+"\t"+outputletter+"\t"+str(outpos)+"\t",

            (inputletter, outputletter, outpos, coord_mr) = self.rotor_m.reflectCipher(outpos)
            self.drawing_list.append(coord_mr[0])
            self.drawing_list.append(coord_mr[1])
            if showoutput:
                print inputletter+"\t"+outputletter+"\t"+str(outpos)+"\t",
                
            (inputletter, outputletter, outpos, coord_rr) = self.rotor_r.reflectCipher(outpos)
            self.drawing_list.append(coord_rr[0])
            self.drawing_list.append(coord_rr[1])
            if showoutput:
                print inputletter+"\t"+outputletter+"\t"+str(outpos)+"\t",
                print chr(outpos+65),
            crypto.append(chr(outpos+65))

        if showoutput:
            print
            print
        return (''.join(crypto), coord_r, coord_rr)

    def show(self, surface):
        self.rotor_r.show(surface)
        self.rotor_m.show(surface)
        self.rotor_l.show(surface)
        self.reflector.show(surface)
        if self.drawing_list:
            line_counter = 0
            start_point = self.drawing_list[0]
            for end_point in self.drawing_list:
                if line_counter < 8:
                    pygame.draw.line(surface,(255,0,0), start_point, end_point, 2)
                else:
                    pygame.draw.line(surface,(0,255,0), start_point, end_point, 2)
                line_counter +=1
                start_point = end_point

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

    def show(self, surface):
        pygame.draw.rect(surface,self.back_color, self.rect)
        if self.bordered:
            pygame.draw.rect(surface, (0,0,0), self.rect, 2)
            
        y = self.y + (self.height - self.thetext.get_height())/2

        if self.centered:
            x = self.x + (self.width - self.thetext.get_width())/2
        else:
            x = self.x

        surface.blit(self.thetext,(x, y))

class PlugBoard(object):
    def __init__(self, plugs):
	# A standard A-Z list using comprehension

        self.letters = [chr(i) for i in range(65,91)]

        # Create two dictionaries for forward and reverse
        # ciphering, each letter corresponding to itself
        # unless modified by the plugs dict

        self.translation_dict = dict(zip(self.letters, self.letters))
    
	# Modify the forward dictionary according to plugs

        for i in plugs.iterkeys():
            self.translation_dict[i]=plugs[i]

	# Create a reverse plugs dictionary

        reverse_plugs = dict((value, key) for key,value in plugs.iteritems())

        # Modify the reverse dictionary according to reverse_plugs

        for i in reverse_plugs.iterkeys():
            self.translation_dict[i]=reverse_plugs[i]

    def cipher(self,letter):
        return self.translation_dict[letter]
     
def main():

    # Initialize pygame library

    pygame.init()

    # Basic settings / objects

    # Rotor starting positions (left, medium, right)
    
    rotor_l_start = 'A'
    rotor_m_start = 'A'
    rotor_r_start = 'A'

    # Reflector, either 'B' or 'C'
    
    reflector_type = 'B'

    # Ring settings (left, medium, right)
    
    ring_setting_l = 1
    ring_setting_m = 1
    ring_setting_r = 1

    # Rotor assembly consists of the three rotors
    # Additional optional parameters are set to default values
    
    rotor_assembly = RotorAssembly(rotor_l_start,rotor_m_start,rotor_r_start,
                                   reflector_type, ring_setting_l,
                                   ring_setting_m, ring_setting_r)

    # Initialize the pygame window

    surfacecolor = (50,80,250)
    screen = pygame.display.set_mode((swidth, sheight), DOUBLEBUF, 32)
    pygame.display.set_caption("The Enigma, Reborn!")

    # Create objects

    # Create the text boxes that hold input / output lines
    
    inputbox = TextBox(0, sheight - 80, swidth-120, 40, (255,0,0), (255,255,255)," Input: ")
    outputbox = TextBox(0, sheight - 40, swidth-120, 40, (0,255,0), (255,255,255)," Output: ")

    # Create small textboxes that connect to input / output of the rightmost rotor
    
    smallinput = TextBox(swidth - 60, sheight -140, 40,40, (255,0,0), (255,255,255), centered = True)
    smalloutput = TextBox(swidth - 60, 20, 40, 40, (0,255,0), (255,255,255), centered = True)

    infobox = TextBox(0,0, swidth, 40, surfacecolor, (255,255,255), " Rotor positions: ")
    
    # Create small textboxes that act as clickable buttons to change rotor positions

    x = 10 + infobox.getTextWidth()
    y = 5
    rotate_l = TextBox(x, y, 30,30, (255,255,0), (0,0,255), rotor_l_start, bordered = True, centered = True)
    x = x + 5 + rotate_l.getRectWidth()
    rotate_m = TextBox(x,y,30,30, (255,255,0), (0,0,255), rotor_m_start, bordered = True, centered = True)
    x = x + 5 + rotate_m.getRectWidth()
    rotate_r = TextBox(x,y, 30,30, (255,255,0), (0,0,255), rotor_r_start, bordered = True, centered = True)

    # Ditto for ring settings

    x = x + 5 + rotate_r.getRectWidth()
    infobox2 = TextBox(x, 0, swidth, 40, surfacecolor, (255,255,255), " Ring Settings: ")
    x = x + 10 + infobox2.getTextWidth()
    rsetting_l = TextBox(x, y, 30, 30, (255,255,0), (0,0,255), str(ring_setting_l), bordered = True, centered = True)
    x = x + 5 + rsetting_l.getRectWidth()
    rsetting_m = TextBox(x, y, 30, 30, (255,255,0), (0,0,255), str(ring_setting_m), bordered = True, centered = True)
    x = x + 5 + rsetting_m.getRectWidth()
    rsetting_r = TextBox(x, y, 30, 30, (255,255,0), (0,0,255), str(ring_setting_r), bordered = True, centered = True)

    # Finally, show reflector

    x = x + 10 + rsetting_r.getRectWidth()
    infobox3 = TextBox(x, 0, swidth, 40, surfacecolor, (255,255,255), "Reflector type: ")
    x = x + 10 + infobox3.getTextWidth()
    reflector_l = TextBox(x,y, 30, 30, (255,255,0), (0,0,255), reflector_type, bordered = True, centered = True)
    
    # clearbox is a button that resets input / output text lines
    
    clearbox = TextBox(swidth-100, sheight-80, 80,38, (255,255,0), (0,0,255),"Clear", bordered = True, centered = True)
    resetbox = TextBox(swidth-100, sheight-40, 80,38, (255,255,0), (0,0,255),"Reset", bordered = True, centered = True)

    # This list contains all text objects (except buttons) so we can handle them all at once
    
    all_objects = [ inputbox, outputbox,  clearbox, resetbox,
                    infobox, infobox2, infobox3, rotate_l, rotate_m, rotate_r, reflector_l,
                    rsetting_l,rsetting_m, rsetting_r, smallinput, smalloutput ]

    clickable_objects = [ rotate_l, rotate_m, rotate_r,
                         rsetting_l, rsetting_m, rsetting_r,
                         reflector_l, resetbox ]


    # Begin main loop
    
    coord_r = []
    coord_rr = []
    cipher = []
    cleartext = []
    plugs = {'A':'F', 'B':'X', 'C':'L', 'O':'R', 'M':'U','D':'Y','I':'K','E':'N',
             'G':'H','S':'W'}
    board = PlugBoard(plugs)
    framerate = 50
    clock = pygame.time.Clock()
    endprogram = False
    
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
                character = board.cipher(character)
                smallinput.setText(character)
                (output, coord_r, coord_rr)  = rotor_assembly.cipher(character, False)
                output = board.cipher(output)
                cipher.append(output)
                outputbox.setText(" Output: "+''.join(cipher))
                smalloutput.setText(output)
                rotate_l.setText(rotor_assembly.rotor_l.getPosition())
                rotate_m.setText(rotor_assembly.rotor_m.getPosition())
                rotate_r.setText(rotor_assembly.rotor_r.getPosition())
                
          if event.type == MOUSEBUTTONDOWN:
                if clearbox.getClicked():

                  # Clicking clear button simply clears the main input / output areas
                  
                  cleartext = []
                  cipher = []
                  inputbox.setText(" Input: ")
                  outputbox.setText(" Output: ")
                else:
                    # All other clickable objects in the resetting_objects list
                    # clear all input, output and highlights
                    for theobject in clickable_objects:
                        if theobject.getClicked():
                            rotor_assembly.resetHighlightsAndDrawings()
                            coord_r = []
                            coord_rr = []
                            cleartext = []
                            cipher = []
                            inputbox.setText(" Input: ")
                            outputbox.setText(" Output: ")
                            smallinput.clearText()
                            smalloutput.clearText()
                            break

                  
                    if rotate_l.getClicked():
                        rotor_assembly.rotor_l.rotate()
                        rotate_l.setText(rotor_assembly.rotor_l.getPosition())
                    elif rotate_m.getClicked():
                        rotor_assembly.rotor_m.rotate()
                        rotate_m.setText(rotor_assembly.rotor_m.getPosition())
                    elif rotate_r.getClicked():
                        rotor_assembly.rotor_r.rotate()
                        rotate_r.setText(rotor_assembly.rotor_r.getPosition())
                    elif rsetting_l.getClicked():
                        rotor_assembly.rotor_l.increaseRingSetting()
                        rsetting_l.setText(str(rotor_assembly.rotor_l.getRingSetting()))
                    elif rsetting_m.getClicked():
                        rotor_assembly.rotor_m.increaseRingSetting()
                        rsetting_m.setText(str(rotor_assembly.rotor_m.getRingSetting()))
                    elif rsetting_r.getClicked():
                        rotor_assembly.rotor_r.increaseRingSetting()
                        rsetting_r.setText(str(rotor_assembly.rotor_r.getRingSetting()))
                    elif reflector_l.getClicked():
                        if rotor_assembly.reflector.getType() == 'B':
                            rotor_assembly.reflector.setType('C')
                        else:
                            rotor_assembly.reflector.setType('B')
                        reflector_l.setText(rotor_assembly.reflector.getType())
                    elif resetbox.getClicked():

                        # Recreate the rotor_assembly object, resetting it to initial values
                        
                        rotor_assembly = RotorAssembly(rotor_l_start,rotor_m_start,rotor_r_start,
                                                       reflector_type, ring_setting_l,
                                                       ring_setting_m, ring_setting_r)

                        # Reset the other boxes too
                        
                        rotate_l.setText(rotor_assembly.rotor_l.getPosition())    
                        rotate_m.setText(rotor_assembly.rotor_m.getPosition())
                        rotate_r.setText(rotor_assembly.rotor_r.getPosition())
                        rsetting_l.setText(str(rotor_assembly.rotor_l.getRingSetting()))
                        rsetting_m.setText(str(rotor_assembly.rotor_m.getRingSetting()))
                        rsetting_r.setText(str(rotor_assembly.rotor_r.getRingSetting()))
                        reflector_l.setText(rotor_assembly.reflector.getType())

                    
            


        # fill screen with bluish tint

        screen.fill(surfacecolor)

        # Show the rotor assembly

        rotor_assembly.show(screen)
        
        # Show all other objects
        
        for theobject in all_objects:
            theobject.show(screen)

                        
        if coord_r:
            pygame.draw.line(screen,(255,0,0), coord_r[0], smallinput.getXY(),2)
        if coord_rr:
            pygame.draw.line(screen, (0,255,0), coord_rr[1], smalloutput.getXY(),2)
            
        time = clock.tick(framerate)
        pygame.display.update()

    # shutdown pygame and exit program
    
    pygame.quit()
    exit()

# Start program
if __name__ == "__main__":
    main()

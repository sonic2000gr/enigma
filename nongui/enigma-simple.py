# -*- coding: utf-8 -*-

class Reflector(object):
    def __init__(self, type='B'):
        self.type = type
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
                
    def reflect(self, position):
        if position >=0 and position <=25:
            return self.reflection_table[position]
        

class Rotor(object):
    def __init__(self, startposition,placement):
       self.letter_ring = [ 'A', 'B', 'C', 'D', 'E',
                        'F', 'G', 'H', 'I', 'J',
                        'K', 'L', 'M', 'N', 'O',
                        'P', 'Q', 'R', 'S', 'T',
                        'U', 'V', 'W', 'X', 'Y', 'Z']
       self.placement = placement
       #
       # Get a number from letter, ie 'A' = 65 - 65 = 0, B = 66-65 = 1 etc.
       #
       self.position = ord(startposition) - 65
       #
       # Rotate rotor to starting position
       #
       for i in range(0, self.position):
           self.rotate()

    def rotate(self):
        self.position +=1
        if self.position == 26:
            self.position = 0
        #
        # Rotate both visible letter window
        # and internal coding 
        #
        self.connections = self.connections[1:]+self.connections[0:1]
        self.letter_ring = self.letter_ring[1:] + self.letter_ring[0:1]

    def cipher(self, letter):
        #
        # Rotate before ciphering
        # if rotor is used in rightmost position (placement == Right)
        #
        if self.placement == 'Right':
            self.rotate()
        inputletter = self.letter_ring[letter]
        outputletter = self.connections[letter]
        outputindex = self.letter_ring.index(outputletter)
        return (inputletter, outputletter, outputindex)

    def reflectCipher(self, letter):
        inputletter = self.letter_ring[letter]
        outputindex = self.connections.index(inputletter)
        outputletter = self.letter_ring[outputindex]
        return (inputletter, outputletter, outputindex)

    def getPosition(self):
        return self.letter_ring[0]


class RotorIII(Rotor):
    def __init__(self, startposition,placement='Right'):
        self.connections  = ['B','D','F','H','J','L','C',
                             'P','R','T','X','V','Z','N',
                             'Y','E','I','W','G','A','K',
                             'M','U','S','Q','O']

        super(RotorIII,self).__init__(startposition,placement)

def main():
    themessage=raw_input("Enter message:")
    themessage=themessage.upper()
    print "Encrypting: ",themessage
    rotor_r = RotorIII("A")
    reflector = Reflector("B")
    crypto = list()
    print "III\tIn\tOut\tPos\tR3-In\tR3-Out\tR3-Pos\tEncryptedLetter"
    for letter in themessage:
        (inputletter,outputletter,outpos)= rotor_r.cipher(ord(letter)-65)
        print rotor_r.getPosition()+"\t"+inputletter+"\t"+outputletter+"\t"+str(outpos)+"\t",
        outpos = reflector.reflect(outpos)
        (inputletter, outputletter, outpos) = rotor_r.reflectCipher(outpos)
        print inputletter+"\t"+outputletter+"\t"+str(outpos)+"\t",
        print chr(outpos+65)
        crypto.append(chr(outpos+65))

    print "".join(crypto)

if __name__=="__main__":
    main()

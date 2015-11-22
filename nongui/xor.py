#! /usr/bin/env python

key = [2, 7, 3, 4, 9, 1]
keypos = 0
thetext = raw_input("Enter text:")
thetext = thetext.upper()
ciphertext = ""
for letter in thetext:
    ciphertext += chr(ord(letter) ^ key[keypos])
    keypos +=1
    if keypos==6:
        keypos=0
print ciphertext

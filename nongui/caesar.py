#! /usr/bin/env python
#
# Simple Caesar cipher
# (shifts 3 places to the right)
# we of course prefer Ceasar salads)
#

plaintext = raw_input("Enter text:")
plaintext = plaintext.upper()
ciphertext = ""
for letter in plaintext:
    if ord(letter)>=65 and ord(letter)<=90:
      newletter = ord(letter) + 3
      if newletter > 90:
          newletter = newletter - 26
      ciphertext += chr(newletter)
    else:
      ciphertext += " "
print ciphertext

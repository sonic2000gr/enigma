#! /usr/bin/env python

thetext = raw_input("Enter text:")
thetext = thetext.upper()
frequencylist = [ 0 for i in range(26)]
for letter in thetext:
    letterord = ord(letter)
    if letterord>= 65 and letterord<=90:
      letterord -= 65
      frequencylist[letterord] += 1
print frequencylist

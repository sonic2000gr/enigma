/* Nano Enigma 
   Version 1.1
   With LCD support
   (C) 2015 Manolis Kiagias
   The Enigma Project 
   Licensed under the BSD license */

/* LCD Connections:

1.  Vss => GND
2.  Vdd => 5V
3.  Vo  => 10K wiper (connected to 5V - GND)
4.  RS  => D12
5.  RW  => GND
6.  E   => D11
11. D4  => D10
12. D5  => D9
13. D6  => D8
14. D7  => D7
15. A   => 5V
16. K   => GND */

/* LED Connections to D2 - D6. D2 is LSB */

#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 10, 9, 8, 7);

int rotorIII[] = { 1, 3, 5, 7, 9, 11, 2, 15, 17, 19,
                   23, 21, 25, 13, 24, 4, 8, 22, 6, 0,
                   10, 12, 20, 18, 16, 14 };
                     
int reflector[] = { 24, 17, 20, 7, 16, 18, 11,
                    3, 15, 23, 13, 6, 14, 10,
                    12, 8, 4, 1, 5, 25, 2, 22,
                    21, 9, 0, 19};

void setup() {
 
 /* Initialize serial communications */
  
 Serial.begin(9600);
 
 /* Initialize LED outputs */
 
 for (int i=2; i<=6; i++)
   pinMode(i,OUTPUT);
 
 /* Show welcome message */
 
 lcd.begin(16,2);
 lcd.clear();
 lcd.setCursor(0, 0);
 lcd.print("The Enigma");
 lcd.setCursor(0,1); 
 lcd.print("EPAL Kissamou");
 delay(3000);
 lcd.setCursor(0,1);
 lcd.print("(C) 2015-2016");
 delay(3000);
 lcd.clear();
 lcd.setCursor(0,0);
 lcd.print("Enigma Ready");
 lcd.setCursor(0,1);
 lcd.print(">");
 Serial.println("Enigma Ready");
 Serial.print("Enter letter: ");
}


void loop() {
  char c;
  int output, refout, rev;
  int keyboardindex;
  
  /* Read letter from serial if available */
  
  if (Serial.available()) {
    c = Serial.read();
    Serial.println(c);
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print(">");
    lcd.setCursor(1,0);
    lcd.print(c);
    lcd.setCursor(0,1);
    lcd.print("Cipher: ");
    lcd.setCursor(8,1); 
    Serial.println("Results: ");
    keyboardindex = validateLetter(c);
    if (keyboardindex!=31) {
      output = encryptRotorIII(keyboardindex);
      refout=reflect(output);
      rev=reverseEncryptRotorIII(refout);
      showInt(rev+1); 
      lcd.print((char)(rev+65)); 
    } else {
      Serial.println("Invalid input!");
      lcd.print("Invalid!");
    }
    Serial.print("Enter letter: ");
  }
}

/* Convert number to binary and
   show on 5 LEDs */
   
void showInt(int c)
{
  char s[6];
  char letter = c + 64;
  int i=0;
  if (c >= 1 && c <= 31) {
    /* initialize array */
 
    for (i = 0; i <= 4; i++)
      s[i]='0';
 
    /* Terminate char array properly to be printed
      by Serial.println */
      
    s[5]='\0';
    
    /* Convert to binary */
    
    i=4;
    while (c >= 1) {
      if  (c % 2 == 1)
        s[i--] = '1';
      else
        s[i--] = '0';
      c = c / 2;
    }
  
    /* Display in LEDs 
       Outputs to D2-D6 */
       
    for (i = 2; i <= 6; i++)
      if  (s[6-i] == '0')
        digitalWrite(i, LOW);
      else
        digitalWrite(i, HIGH);
    Serial.print("Binary: ");  
    Serial.println(s);
    Serial.print("Letter: ");
    Serial.println(letter);
  } else
    Serial.println("Error!");
}

/* Rotate RotorIII by one position
   Taking care of wrap arounds */
   
void rotateRotorIII()
{
  /* Store the value of first element */
  int temp = rotorIII[0];
  int i;
  /* Shift elements one up */
  for (i=0; i<=24; i++)
    rotorIII[i] = rotorIII[i+1];
  /* Move first element to bottom */
  rotorIII[25] = temp;
  /* Shift the coding one up
     Wrap around if needed */
  for (i=0; i<=25; i++) {
    rotorIII[i] = rotorIII[i] - 1;
    if (rotorIII[i]<0) 
       rotorIII[i] = 25;
  }
}

int encryptRotorIII(int keyboardindex) {   
	
        /* Since this is the rightmost rotor,
	   rotate before encrypting! */
	   
	rotateRotorIII();
	
	/* return output position */
	
	return rotorIII[keyboardindex];
}


int validateLetter(char letter) 
{
 if (letter >=97 && letter <= 122)
   letter = letter - 97;
 else
   letter = letter - 65;
	    
 if (letter <0 || letter >25) 
   return 31;
 else
   return letter;
}

int reflect(int index) 
{
	if ( index>=0 && index <=25)
	  return reflector[index];
	else
	  return 31;
}

/* Reverse encrypt letter from reflector 
   through RotorIII */
   
int reverseEncryptRotorIII(int pos)
{
  int output=0;
  int found=0;
  
  while (output <= 25 && found == 0) {
  	if (rotorIII[output] == pos) 
  	   found = 1;
  	else
  	   output++;
  } 
  return output;
}

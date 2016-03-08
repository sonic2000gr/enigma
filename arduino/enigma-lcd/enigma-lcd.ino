/* Nano Enigma 
   Version 1.2
   With LCD support
   (C) 2015-2016 Manolis Kiagias
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

#define TRUE 1
#define FALSE 0
#include <LiquidCrystal.h>

// LCD pins 

LiquidCrystal lcd(12, 11, 10, 9, 8, 7);

// Notches for rotors 0 (left), 1 (middle), 2 (right)

int notch[] = {17, 5, 22};

// Initial rotor positions

int rotpos[] = { 0, 0, 0 };

// For Double Stepping

int just_rotated = FALSE;

// Rotor tables

int rotor[3][26] =  {
                     { 4, 10, 12, 5, 11, 6, 3, 16,
                       21, 25, 13, 19, 14, 22, 24, 7,
                       23, 20, 18, 15, 0, 8, 1, 17,
                       2, 9 },
				 
		     { 0, 9, 3, 10, 18, 8, 17, 20,
                       23, 1, 11, 7, 22, 19, 12, 2,
                       16, 6, 25, 13, 15, 24, 5, 21,
                       14, 4 },

                     { 1, 3, 5, 7, 9, 11, 2, 15, 17, 19,
                       23, 21, 25, 13, 24, 4, 8, 22, 6, 0,
                       10, 12, 20, 18, 16, 14 } };

// Type B reflector
                     
int reflector[] = { 24, 17, 20, 7, 16, 18, 11,
                    3, 15, 23, 13, 6, 14, 10,
                    12, 8, 4, 1, 5, 25, 2, 22,
                    21, 9, 0, 19 };

void setup()
{

  /* Initial rotor positions */
  /* Enigma can start in any configuration */
 
  initRotorPos('A',2);
  initRotorPos('A',1);
  initRotorPos('A',0);

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


void loop()
{
  char c,d;
  int output, refout, rev;
  int keyboardindex;
  
  /* Read letter from serial if available */
  
  if (Serial.available()) {
    c = Serial.read();
    if (c == '!') {
      lcd.clear();
      
      // Rotate rotors until position 0 is reached
      for (int i=0; i<=2; i++)
        while (rotpos[i]!=0)
          rotateRotor(i);
      lightsOff();
      lcd.setCursor(0,0);
      lcd.print("Machine Reset!");
      Serial.println("");
      Serial.println("Machine Reset!");
      Serial.print("Enter letter: ");
      lcd.setCursor(0,1);
      lcd.print(">");
    } else {
    Serial.println(c);
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print(">");
   
    Serial.println("Results: ");
    keyboardindex = validateLetter(c);
    if (keyboardindex!=31) {
      d = keyboardindex + 65;
      lcd.setCursor(1,0);
      lcd.print(d);
      output = encryptRotor(keyboardindex,2);
      output = encryptRotor(output,1);
      output = encryptRotor(output, 0);
      refout = reflect(output);
      rev = reverseEncryptRotor(refout,0);
      rev = reverseEncryptRotor(rev, 1);
      rev = reverseEncryptRotor(rev,2);
      showInt(rev+1); 
      lcd.setCursor(0,1);
      lcd.print("Cipher: ");
      lcd.setCursor(8,1); 
      lcd.print((char)(rev+65)); 
    } else {
      Serial.println("Invalid input!");
      lcd.print("Invalid!");
      showInt(31);
    }
    Serial.print("Enter letter: ");
  }
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

// Turn off all LEDs

void lightsOff()
{
  for (int i=2; i<=6; i++)
    digitalWrite(i, LOW);
}

/* Rotate Rotor by one position
   Taking care of wrap arounds */
   
void rotateRotor(int rotorno)
{
  int i;
  int temp;
    
  /* Keep the top element */
	
  temp = rotor[rotorno][0];
	
  /* Shift all elements one up */
	
  for (i=0; i<=24; i++)
    rotor[rotorno][i] = rotor[rotorno][i+1];
	
  /* Add the first element to the bottom */
	    
  rotor[rotorno][25] = temp;
	
  /* Reduce the values by 1
     Wrap around if necessary  */
	
  for (i=0; i<=25; i++) {
    rotor[rotorno][i] = rotor[rotorno][i] - 1;
    if (rotor[rotorno][i]< 0) 
      rotor[rotorno][i] = 25;
  }    

  if (++rotpos[rotorno]==26)
    rotpos[rotorno] = 0;
}

int encryptRotor(int keyboardindex, int rotorno)
{
  /* If this is the rightmost rotor,
     rotate before encrypting! */

  /* Rotate middle and left rotors too
     Take care of the double stepping bug */
	
  if (rotorno==2)  {
    rotateRotor(rotorno);
    if (rotpos[1]==notch[1]-1) {
      rotateRotor(1);
      rotateRotor(0);
      just_rotated = TRUE;
    } else
      just_rotated = FALSE;   
      if (rotpos[2] == notch[2] && !just_rotated)  {
        rotateRotor(1);
      }
  }
	
  /* return output position */
	
  return rotor[rotorno][keyboardindex];
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
   
int reverseEncryptRotor(int pos, int rotorno)
{
  int output=0;
  int found=0;
  
  while (output <= 25 && found == 0) {
    if (rotor[rotorno][output] == pos) 
      found = 1;
    else
      output++;
  }
  return output;
}

/* Initialize Rotor to position indicated by letter */

void initRotorPos(char p, int rotorno)
{
  int i,j;
  i = validateLetter(p);
  for (j=1; j<=i; j++) 
    rotateRotor(rotorno);
}

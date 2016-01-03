/* Nano Enigma 
   Version 1.0
   (C) 2015 Manolis Kiagias
   The Enigma Project 
   Licensed under the BSD license */


char rotorIII[] = {'B','D','F','H','J','L','C','P','R','T',
                   'X','V','Z','N','Y','E','I','W','G','A',
                   'K','M','U','S','Q','O','\0'};
                
void setup() {
 
 /* Initialize serial communications */
  
 Serial.begin(9600);
 Serial.println("Enigma Ready");
 
 /* Initialize outputs 2 to 6
    Connect five LEDs to outputs D2 - D6
    via 330 Ohm resistors to GND */    

 for (int i=2; i<=6; i++)
   pinMode(i,OUTPUT);
 Serial.print("Enter letter: ");
}


void loop() {
  char c;
  int r1out;
  
  /* Read letter from serial if available */
  
  if (Serial.available()) {
    c = Serial.read();
    Serial.println(c); 
    Serial.print("Result: ");
    r1out = encryptRotorIII(c);
    showInt(r1out);
    Serial.print("Encrypted:");
    Serial.println((char)(r1out+64));
    Serial.print("Enter letter: ");
  }
}


void showInt(int c)
{
  char s[6];
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
      
    Serial.println(s);
  } else
    Serial.println("Error!");
}

void rotateRotorIII()
{
 int i=0;
 char t;

 // Get the letter at first position

 t=rotorIII[0]; 

 // Move all letters one position up

 for (i=1; i<=25; i++)
   rotorIII[i-1]=rotorIII[i];

 // Add the letter at the end
 
 rotorIII[25]=t;
}

int encryptRotorIII(char letter)
{
 
  // Convert small english to capitals
  // if necessary 
  
  if (letter >= 95 && letter <= 122)
    letter = letter - 96;
  else
    letter = letter - 64;
 
  // Check it is a valid letter!
  // If not, light up all LEDS
  
  if (letter < 1 || letter > 26)
     return 31;
 
  // Rotate the rotor before encrypting!
  
  rotateRotorIII(); 
  return rotorIII[letter-1]-64;
}

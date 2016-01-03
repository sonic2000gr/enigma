/* Mini Enigma 
   Version 0.1
   (C) 2015 Manolis Kiagias
   The Enigma Project 
   Licensed under the BSD license */


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
  
  /* Read letter from serial if available */
  
  if (Serial.available()) {
    c = Serial.read();
    Serial.println(c); 
    Serial.print("Result: ");
    
    /* Convert to binary and display */
    
    showInt(c);
    Serial.print("Enter letter: ");
  }
}

void showInt(int c)
{
  char s[6];
  int i=0;
 
  /* convert lower case to upper case if needed */
 
  if (c >= 95 && c <= 122)
    c = c - 96;
  else
    c = c - 64;
 
  /* if not in letter range, do not encode */
 
  if (c >= 1 && c <= 26) {
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

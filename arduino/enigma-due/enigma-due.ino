/* The Enigma Due - Motor Control
   Version 1.0
   With LCD, motors and reflector LED board support
   (C) 2015-2016 Manolis Kiagias
   The Enigma Project 
   Licensed under the BSD license */

/* LCD Connections:

  LCD    Arduino
==================
  Vss    GND
  Vdd    5V
  Vo     10K wiper (connected to 5V - GND)
  RS     D12
  RW     GND
  E      D11
  D4     D10
  D5     D9
  D6     D8
  D7     D7
  A      5V
  K      GND 
  
*/

#include <LiquidCrystal.h>
#define TRUE 1
#define FALSE 0
#define EXTRAPULSES 1
#define FULLROT 6
#define STEPCOUNT 156
#define MOTORDELAY 3
#define HASHPIN 35

// Right Rotor  DUE pins (A3, A2, A1, A0)

#define R3_IN4 60
#define R3_IN3 61
#define R3_IN2 68
#define R3_IN1 69

//Middle Rotor DUE pins (D3, D2, D1, D0)

#define R2_IN4 28
#define R2_IN3 27
#define R2_IN2 26
#define R2_IN1 25

//Left Rotor DUE pins (C8, C7, C6, C5)

#define R1_IN4 40
#define R1_IN3 39
#define R1_IN2 38
#define R1_IN1 37

// Reflector Pins
// A =54, B=55, ... , Z =?

int reflectorPins[] = { 54, 55, 56, 57, 58, 59,
                        62, 63, 64, 65, 66, 67,
                        44, 46, 48, 50, 52, 53,
                        51, 49, 47, 45, 43, 41,
                        31, 33 };

// Stepper motor states
// These will have to be multiplied by 32
// for the left Rotor since Port pins start with C5

int states[] = { B1000,
                 B1100,
                 B0100,
                 B0110,
                 B0010,
                 B0011,
                 B0001,
                 B1001};
                 

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

/* Stepper motor states
   Stepper motors restart from the last state
   each movement */
   
int currentstate3 = 0;
int currentstate2 = 0;
int currentstate1 = 0;

/* Letter count to correct for missing 14 pulses per full rotation */

int stepmod3 = 0;
int stepmod2 = 0;
int stepmod1 = 0;
int lettercount3 = 0;
int lettercount2 = 0;
int lettercount1 = 0;


void setup()
{
  char c;
  
  // Initialize Serial Comms
  
  Serial.begin(9600);

  // Initialize rotor pins for motors
  
  initRotorPins();
  
  // Initialize reflector lamp pins
  
  initReflectorPins();
  
  // Turn off all reflector LEDs
  
  reflectorOff();
  
  /* Initial rotor positions */
  /* Enigma can start in any configuration */
 
  initRotorPos('A',2);
  initRotorPos('A',1);
  initRotorPos('A',0);
 
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
  delay(2000);
  
  // Test motors and reflector
  
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Enigma Testing");
  lcd.setCursor(0,1);
  lcd.print("Right Motor     ");
  for(int j=0; j<=25; j++)
    motor3NextLetter();
  motor3Stop();
  lcd.setCursor(0,1);
  lcd.print("Middle Motor    ");
  for(int j=0; j<=25; j++)
    motor2NextLetter();
  motor2Stop();
  lcd.setCursor(0,1);
  lcd.print("Left Rotor      ");
  for(int j=0; j<=25; j++)
    motor1NextLetter();
  motor1Stop();
  lcd.setCursor(0,1);
  lcd.print("Reflector LEDs  ");
  for (int j=0; j<=25; j++) {
    digitalWrite(reflectorPins[j], HIGH);
    delay(100);
    digitalWrite(reflectorPins[j], LOW);
  }
  digitalWrite(HASHPIN, HIGH);
  delay(100);
  digitalWrite(HASHPIN, LOW);
  // lcd.clear();
  // lcd.print("Enter RotorA Pos");
  // lcd.setCursor(0,1);
  // Serial.println("Enter RotorA Pos:");
  // c = Serial.read();
  
  // Start crypto 
  
  lcd.clear();
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
      lcd.setCursor(0,0);
      reflectorOff();
      lcd.print("Resetting...");
      for (int i=0; i<=2; i++) {
        while (rotpos[i]!=0) {
          switch(i) {
            case 0:
              motor1NextLetter();
              break;
            case 1:
              motor2NextLetter();
              break;
            case 2:
              motor3NextLetter();
              break;
            default:
              break;
          } 
          rotateRotor(i);
        }
        switch(i) {
            case 0:
              motor1Stop();
              break;
            case 1:
              motor2Stop();
              break;
            case 2:
              motor3Stop();
              break;
            default:
              break;
          } 
      }
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
      delay(2000);
      rev = reverseEncryptRotor(refout,0);
      rev = reverseEncryptRotor(rev, 1);
      rev = reverseEncryptRotor(rev,2);
      result(rev);
      showInt(rev+1); 
      lcd.setCursor(0,1);
      lcd.print("Cipher: ");
      lcd.setCursor(8,1); 
      lcd.print((char)(rev+65));
      delay(1000);
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
 
    Serial.print("Binary: ");  
    Serial.println(s);
    Serial.print("Letter: ");
    Serial.println(letter);
  } else
    Serial.println("Error!");
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
    motor3NextLetter();
    motor3Stop();
    rotateRotor(rotorno);
    if (rotpos[1]==notch[1]-1) {
      rotateRotor(1);
      motor2NextLetter();
      motor2Stop();
      rotateRotor(0);
      motor1NextLetter();
      motor1Stop();
      just_rotated = TRUE;
    } else
      just_rotated = FALSE;   
      if (rotpos[2] == notch[2] && !just_rotated)  {
        motor2NextLetter();
        motor2Stop();
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
  if ( index>=0 && index <=25) {
    reflectorOff();
    digitalWrite(reflectorPins[index], HIGH);
    digitalWrite(reflectorPins[reflector[index]],HIGH);
    return reflector[index];
  }
  else
    return 31;
}

int result(int index)
{
   if (index>=0 && index<=25) {
      reflectorOff();
      digitalWrite(reflectorPins[index], HIGH);
      digitalWrite(HASHPIN, HIGH);
   }       
}

void reflectorOff() {
  for (int j=0; j<=25; j++)
     digitalWrite(reflectorPins[j], LOW);
  digitalWrite(HASHPIN, LOW);
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

void motor3NextLetter() {
  
      // Adjust for missing pulses on full rotation
     
     int stepcount;
     if (stepmod3 == 1) {
        stepcount = STEPCOUNT + EXTRAPULSES;
        stepmod3 = 0;
     } else {
        stepmod3 = 1;
        stepcount = STEPCOUNT;
     }

     if (++lettercount3 == 25) {
       lettercount3 = 0;
       stepcount += FULLROT;
     }
     
     for (int j=0; j<stepcount; j++) {
       REG_PIOA_ODSR = states[currentstate3]; 
       if (++currentstate3 == 8) currentstate3 = 0;
       delay(MOTORDELAY);
     }
}

void motor2NextLetter(){
    // Adjust for missing pulses on full rotation
     
     int stepcount;
     if (stepmod2 == 1) {
        stepcount = STEPCOUNT + EXTRAPULSES;
        stepmod2 = 0;
     } else {
        stepcount = STEPCOUNT;
        stepmod2 = 1;
     }

     if (++lettercount2 == 25) {
       lettercount2 = 0;
       stepcount += FULLROT;
     }


  for (int j=0; j<stepcount; j++) {
    REG_PIOD_ODSR = states[currentstate2]; 
    if (++currentstate2 == 8) currentstate2 = 0;
    delay(MOTORDELAY);
 } 
}

void motor1NextLetter(){
     int stepcount;
     if (stepmod1 == 1) {
        stepcount = STEPCOUNT + EXTRAPULSES;
        stepmod1 = 0;
     } else {
        stepcount = STEPCOUNT;
        stepmod1 = 1;
     }

     if (++lettercount1 == 25) {
       lettercount1 = 0;
       stepcount += FULLROT;
     }

  for (int j=0; j<stepcount; j++) {
    REG_PIOC_ODSR = states[currentstate1]*32; 
    if (++currentstate1 == 8) currentstate1 = 0;
    delay(MOTORDELAY);
  }
}

void initRotorPins() {
  // Initialize rotor 3 pins
  
  pinMode(R3_IN4, OUTPUT);
  pinMode(R3_IN3, OUTPUT);
  pinMode(R3_IN2, OUTPUT);
  pinMode(R3_IN1, OUTPUT);
  REG_PIOA_OWER = 15;
  REG_PIOA_ODSR = 0; 
  
  // Initialize rotor 2 pins
  
  pinMode(R2_IN4, OUTPUT);
  pinMode(R2_IN3, OUTPUT);
  pinMode(R2_IN2, OUTPUT);
  pinMode(R2_IN1, OUTPUT);
  REG_PIOD_OWER = 15;
  REG_PIOD_ODSR = 0; 

  // Intialize rotor 1 pins
  
  pinMode(R1_IN4, OUTPUT);
  pinMode(R1_IN3, OUTPUT);
  pinMode(R1_IN2, OUTPUT);
  pinMode(R1_IN1, OUTPUT);
  REG_PIOC_OWER = 480;
  REG_PIOC_ODSR = 0; 
}

void initReflectorPins() {
  for (int j=0; j<=25; j++)
    pinMode(reflectorPins[j], OUTPUT);
  pinMode(HASHPIN, OUTPUT);
}

void motor3Stop(){
 REG_PIOA_ODSR = 0; 
}

void motor2Stop(){
 REG_PIOD_ODSR = 0; 
}

void motor1Stop(){
 REG_PIOC_ODSR = 0; 
}


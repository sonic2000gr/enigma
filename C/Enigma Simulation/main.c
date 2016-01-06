/* Enigma Simulation
   Debug platform for Arduino code
   (C)2015-2016 Manolis Kiagias
   Licensed under the BSD license */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void rotateRotorIII(void);
int encryptRotorIII(int);
int reverseEncryptRotorIII(int);
int validateLetter(char);
int reflect(int);
char indexToLetter(int);

/* RotorIII internal coding 
   A = 0,..., Z=25 */
   
int rotorIII[] = { 1, 3, 5, 7, 9, 11, 2, 15, 17, 19,
                   23, 21, 25, 13, 24, 4, 8, 22, 6, 0,
                   10, 12, 20, 18, 16, 14 };
                   
/* Type B reflector internal coding */
                   
int reflector[] = { 24, 17, 20, 7, 16, 18, 11,
                    3, 15, 23, 13, 6, 14, 10,
                    12, 8, 4, 1, 5, 25, 2, 22,
                    21, 9, 0, 19 };
                    
                    
int main(int argc, char *argv[]) {
    int output,refout,rev;
	char keyboard[]="AAAAAAAAAA";
	int i;
	int keyboardindex; 
    
    /* Test the Enigma */
    
	printf("Keyboard\tRotorIII out\tReflector out\tReverse III\tLetter\n");
    printf("========================================================================\n");
	for (i=0; i<strlen(keyboard); i++) {
		keyboardindex = validateLetter(keyboard[i]);
		if (keyboardindex < 31) {
   		  output = encryptRotorIII(keyboardindex);
    	  refout = reflect(output);
    	  rev = reverseEncryptRotorIII(refout);
    	  printf("%c\t\t%d\t\t%d\t\t%d\t\t\%c\n",keyboard[i],output,refout,rev,indexToLetter(rev));
        } else
          printf("Invalid character!\n");
	}
   	
	system("pause");
	return 0;
}

void rotateRotorIII()
{
    int i;
    int temp;
    
    /* Keep the top element */
	
	temp = rotorIII[0];
	
	/* Shift all elements one up */
	
    for (i=0; i<=24; i++)
      rotorIII[i] = rotorIII[i+1];
	
	/* Add the first element to the bottom */
	    
    rotorIII[25] = temp;
	
	/* Reduce the values by 1
	   Wrap around if necessary  */
	
	for (i=0; i<=25; i++) {
		rotorIII[i] = rotorIII[i] - 1;
		if (rotorIII[i] < 0) 
		  rotorIII[i] = 25;
	}    
}


/* Forward encrypt through RotorIII */

int encryptRotorIII(int keyboardindex) {

	/* Since this is the rightmost rotor,
	   rotate before encrypting! */
	   
	rotateRotorIII();
	
	/* return output position */
	
	return rotorIII[keyboardindex];
}

/* Convert ASCII A-Z (or a-z) to 0 - 25
   Return 31 if invalid character
   (31 can be used to light up all 31 LEDs
   on the Arduino */

int validateLetter(char letter) 
{
 if (letter >=97 && letter <= 122)
   letter = letter - 97;
 else
   letter = letter - 65;
	    
 if (letter < 0 || letter  > 25) 
   return 31;
 else
   return letter;
}

/* Straight forward reflector function */

int reflect(int index) 
{
	if ( index >= 0 && index <= 25)
	  return reflector[index];
	else
	  return 31;
}

/* Reverse encrypt through RotorIII
   Find the letter on the left side
   of the Rottor. Return the index */
   
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

/* Convert an index of 0 - 25 to a letter A - Z */

char indexToLetter(int index)
{
	return 65+index;
}

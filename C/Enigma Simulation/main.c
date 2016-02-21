/* Enigma Simulation
   Debug platform for Arduino code
   (C)2015-2016 Manolis Kiagias
   Licensed under the BSD license */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TRUE 1
#define FALSE 0

void rotateRotor(int);
int encryptRotor(int,int);
int validateLetter(char);
int reflect(int);
char indexToLetter(int);
int reverseEncryptRotor(int, int);
void initRotorPos(char, int);

/* Rotors internal coding 
   A = 0,..., Z=25 */
 
int notch[] = {17, 5, 22};

int rotpos[] = { 0, 0, 0 };

int just_rotated = FALSE;

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

/* Type B reflector internal coding */
                   
int reflector[] = { 24, 17, 20, 7, 16, 18, 11,
                    3, 15, 23, 13, 6, 14, 10,
                    12, 8, 4, 1, 5, 25, 2, 22,
                    21, 9, 0, 19 };
                    
                    
int main(int argc, char *argv[]) {
    int output,refout,rev;
	char keyboard[]="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA";
	char result[128];
	int i;
	int keyboardindex; 
    
    /* Test the Enigma */
    initRotorPos('A',2);
    initRotorPos('C',1);
    initRotorPos('A',0);
    printf("Initial rotor positions III-II-I: %d\t%d\t%d\n\n",rotpos[2],rotpos[1],rotpos[0]);
	printf("Keyboard\tRotorIII out\tReflector out\tReverse III\tLetter\n");
    printf("========================================================================\n");
	for (i=0; i<strlen(keyboard); i++) {
		keyboardindex = validateLetter(keyboard[i]);
		if (keyboardindex < 31) {
   		  output = encryptRotor(keyboardindex,2);
   		  output = encryptRotor(output,1);
   		  output = encryptRotor(output, 0);
    	  refout = reflect(output);
    	  rev = reverseEncryptRotor(refout,0);
    	  rev = reverseEncryptRotor(rev, 1);
    	  rev = reverseEncryptRotor(rev,2);
    	  printf("%c\t\t%d\t\t%d\t\t%d\t\t\%c\n",keyboard[i],output,refout,rev,indexToLetter(rev));
          result[i]=indexToLetter(rev);
		} else
          printf("Invalid character!\n");
	}
	result[i]='\0';
	printf("\nResult: %s\n\n",result);
	system("pause");
	return 0;
}

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

void initRotorPos(char p, int rotorno) {
	int i,j;
	i = validateLetter(p);
	for (j=1; j<=i; j++) 
	  rotateRotor(rotorno);
}

/* Forward encrypt through RotorIII */

int encryptRotor(int keyboardindex, int rotorno) {

	/* If this is the rightmost rotor,
	   rotate before encrypting! */

    /* Rotate middle and left rotors too
       Take care of the double stepping bug */
	
	if (rotorno==2)  {
	  rotateRotor(rotorno);
	  if (rotpos[1]==notch[1]-1) {
		printf("DS\n");
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

/* Convert an index of 0 - 25 to a letter A - Z */

char indexToLetter(int index)
{
	return 65+index;
}

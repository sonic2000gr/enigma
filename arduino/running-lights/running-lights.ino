/* Τρεχαντήρι 
   Συνδέστε LED με αντιστάσεις στις εξόδους D2-D6
   όπως φαίνεται στο σχήμα του βιβλίου.
   
   (C) 2015 Manolis Kiagias
   The Enigma Project
   Licensed under the BSD License */


void setup() {
  // put your setup code here, to run once:
  for (int i=2; i<=9; i++)
    pinMode(i, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(50);
  digitalWrite(9, LOW);
  digitalWrite(2, HIGH);
  for (int i=3; i<=9; i++) {
    delay(50);
    digitalWrite(i, HIGH);
    digitalWrite(i-1, LOW);
  }
}

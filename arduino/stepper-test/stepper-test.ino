int states[] = { B01000000,
                 B01100000,
                 B00100000,
                 B00110000,
                 B00010000,
                 B00011000,
                 B00001000,
                 B01001000};

void setup() {
  // put your setup code here, to run once:
  DDRD = DDRD | B11111100; 
}

void loop() {
  // put your main code here, to run repeatedly:
  int state  =0;
  for (int j=0; j<157; j++) {
   PORTD = states[state++];
   if (state == 8) state = 0;
   delay(1);
  }
  //}
  delay(1000);
}

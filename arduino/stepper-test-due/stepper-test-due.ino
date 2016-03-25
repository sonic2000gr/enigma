// The states for the stepper motor

int currentstate = 0;
int states[] = { B1000,
                 B1100,
                 B0100,
                 B0110,
                 B0010,
                 B0011,
                 B0001,
                 B1001};
void setup() {
  // put your setup code here, to run once:
  pinMode(60, OUTPUT);
  pinMode(61, OUTPUT);
  pinMode(68, OUTPUT);
  pinMode(69, OUTPUT);
  REG_PIOA_OWER = 15;
  }

void loop() {
  // put your main code here, to run repeatedly:
  for (int j=0; j<157; j++) {
    REG_PIOA_ODSR = states[currentstate]; 
    if (++currentstate == 8) currentstate = 0;
   delay(1);
  }
  delay(1000);
}



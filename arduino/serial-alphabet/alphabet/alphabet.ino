void setup() {
  // put your setup code here, to run once:
 Serial.begin(9600);
 Serial.println("Enigma Ready");
 for (int i=8; i<=12; i++)
   pinMode(i,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  char c;
  if (Serial.available()) {
    Serial.println("Enter letter:");
    c=Serial.read();
    Serial.println(c); 
    Serial.print("Result:");
    showInt(c);
  }
}

void showInt(int c)
{
  char s[6];
  int i=0;
  c = c - 64;
  if (c>=0 && c<=26) {
  for (i=0; i<=4; i++)
    s[i]='0';
  s[5]='\0';
  i=4;
  while (c>=1) {
    if  (c % 2==1)
      s[i--]='1';
    else
      s[i--]='0';
    c = c / 2;
  }
  
  for (i=8; i<=12; i++)
    if  (s[i-8]=='0')
      digitalWrite(i, LOW);
    else
      digitalWrite(i, HIGH);
      
  Serial.println(s);
  } else
  Serial.println("Error!");
}
      

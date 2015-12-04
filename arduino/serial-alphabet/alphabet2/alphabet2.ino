void setup() {
  // put your setup code here, to run once:
 for (int i=8; i<=12; i++)
   pinMode(i,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  int c;
  for (c=0; c<=31; c++) {
    showInt(c);
    delay(60);
  }
  for (c=31; c>=0; c--) {
    showInt(c);
    delay(60);
  }
}

void showInt(int c)
{
  char s[6];
  int i=0;
  if (c>=0 && c<=31) {
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
  }
}
      

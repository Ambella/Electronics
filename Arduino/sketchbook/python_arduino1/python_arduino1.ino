#define LEDR     10
#define LEDG     11
#define LEDB     9

int r, g, b;

void setup()
{
  pinMode(LEDR, OUTPUT);
  pinMode(LEDG, OUTPUT);
  pinMode(LEDB, OUTPUT);
  r = g = b = 0;
  
  Serial.begin(9600);
}

void loop()
{
  if(Serial.available() >= 3)
  {
    r = Serial.read();
    g = Serial.read();
    b = Serial.read();
    Serial.write('1'); // Sync
  }
  analogWrite(LEDR, r);
  analogWrite(LEDG, g);
  analogWrite(LEDB, b);
  //delay(10);
  //Serial.println(r);
}

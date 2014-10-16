void setup() {
  // put your setup code here, to run once:
  pinMode(10, INPUT);                        // Left IR Receiver
  pinMode(9, OUTPUT);                        // Left indicator LED
  Serial.begin(9600); 
  pinMode(3, INPUT);
  pinMode(2, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly: 
  delay(500);
  Serial.print("distance = ");
  int dist = irDistance(9,10);
  Serial.println(dist);
  int pOne = digitalRead(2);
  int pTwo = digitalRead(13);
  Serial.print(pOne);
  Serial.println(pTwo);
}
// IR distance measurement function

int irDistance(int irLedPin, int irReceivePin)
{  
  int distance = 0;
  for(long f = 38000; f <= 42000; f += 1000) {
    distance += irDetect(irLedPin, irReceivePin, f);
  }
  return distance;
}
int irDetect(int irLedPin, int irReceiverPin, long frequency)
{
  tone(irLedPin, frequency, 8);              // IRLED 38 kHz for at least 1 ms
  delay(1);                                  // Wait 1 ms
  int ir = digitalRead(irReceiverPin);       // IR receiver -> ir variable
  delay(1);                                  // Down time before recheck
  return ir;                                 // Return 1 no detect, 0 detect
}  


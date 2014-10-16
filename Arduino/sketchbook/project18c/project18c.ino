// Project 18
int latchPin = 8;
int clockPin= 12;
int dataPin = 11;
int bits[] = {B00000001, B00000010, B00000100, B00001000, B00010000, B00100000, B01000000, B10000000};
void setup(){
  // set pintto output
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
}

void loop(){
  for (int i = 0; i < 8; i++){
    digitalWrite(latchPin, LOW);
    shiftOut2(bits[7-i]);
    shiftOut2(bits[i]);
    //shiftOut2(255-i);
    // setlatchPin to high to lock and send data
    digitalWrite(latchPin, HIGH);
    delay(500);
  }
}

void shiftOut2(byte dataOut){
  boolean pinState;

  digitalWrite(dataPin, LOW);
  digitalWrite(clockPin, LOW);
  
  for (int j = 0; j <=7; j++){
    digitalWrite(clockPin, LOW);
    if (dataOut & (1<<j)){
      pinState = HIGH;
    }
    else {
      pinState = LOW;
    }
    digitalWrite(dataPin, pinState);
    digitalWrite(clockPin, HIGH);
    digitalWrite(dataPin, LOW);
  }
  digitalWrite(clockPin, LOW);
}

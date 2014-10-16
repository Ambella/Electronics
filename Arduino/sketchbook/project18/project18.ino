// Project 18
int latchPin = 8;
int clockPin= 12;
int dataPin = 11;

void setup(){
  // set pintto output
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
}

void loop(){
  for (int i = 0; i < 256; i++){
    digitalWrite(latchPin, LOW);
    shiftOut(i);
    shiftOut(255-i);
    // setlatchPin to high to lock and send data
    digitalWrite(latchPin, HIGH);
    delay(250 );
  }
}

void shiftOut(byte dataOut){
  boolean pinState;

  digitalWrite(dataPin, LOW);
  digitalWrite(clockPin, LOW);
  
  for (int i = 0; i <=7; i++){
    digitalWrite(clockPin, LOW);
    if (dataOut & (1<<i)){
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

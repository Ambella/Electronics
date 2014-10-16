const int pingPin = 10;
const int usTocm = 29;
const int piezoPin = 4;
void setup()                                       // Built-in initialization block
{
  Serial.begin(9600);                              // Open serial connection
} 
void loop()                                        // Main loop auto-repeats
{
  //tone(piezoPin, 3000, 500);
  delay(500);
  Serial.print("distance = ");
  int dist = cmDistance();
  Serial.println(dist);
  
}
int cmDistance()
{
  int distance = 0;                                // Initialize distance to zero    
  do                                               // Loop in case of zero measurement
  {
    int us = ping(pingPin);                        // Get Ping))) microsecond measurement
    distance = convert(us, usTocm);                // Convert to cm measurement
    delay(3);                                      // Pause before retry (if needed)
  }
  while(distance == 0);                            
  return distance;                                 // Return distance measurement
}
int convert(int us, int scalar)
{
    return us / scalar / 2;                        // Echo round trip time -> cm
}

long ping(int pin)
{
  long duration;                                   // Variables for calculating distance
  pinMode(pin, OUTPUT);                            // I/O pin -> output
  digitalWrite(pin, LOW);                          // Start low
  delayMicroseconds(2);                            // Stay low for 2 us
  digitalWrite(pin, HIGH);                         // Send 5 us high pulse
  delayMicroseconds(5);                            
  digitalWrite(pin, LOW);                          
  pinMode(pin, INPUT);                             // Set I/O pin to input 
  duration = pulseIn(pin, HIGH, 25000);            // Measure echo time pulse from Ping)))
  return duration;                                 // Return pulse duration
} 

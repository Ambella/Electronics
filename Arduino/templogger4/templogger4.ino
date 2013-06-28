#include <LiquidCrystal.h>

#include <Wire.h>

#include <Adafruit_BMP085.h>

#include <SD.h>

/*     ---------------------------------------------------------
 *     |  Arduino Experimentation Kit Example Code             |
 *     |  CIRC-10 .: Temperature :. (TMP36 Temperature Sensor) |
 *     ---------------------------------------------------------
 *   
 *  A simple program to output the current temperature to the IDE's debug window 
 * 
 *  For more details on this circuit: http://tinyurl.com/c89tvd 
 */
// declare vars
//TMP36 Pin Variables
LiquidCrystal lcd(9, 8, 7, 6, 5, 4);
int calibrationTime = 30; 
int temperaturePin = 0; //the analog pin the TMP36's Vout (sense) pin is connected to
                        //the resolution is 10 mV / degree centigrade 
                        //(500 mV offset) to make negative temperatures an option
int lightPin = 1;
int ledPinHigh = 3;
int pirPin = 2;
Adafruit_BMP085 bmp;
const int chipSelect = 10;
/*
 * setup() - this function runs once when you turn your Arduino on
 * We initialize the serial connection with the computer
 */
void setup()
{
  Serial.begin(9600);  //Start the serial connection with the copmuter
                       //to view the result open the serial monitor 
  pinMode(chipSelect, OUTPUT);
  pinMode(ledPinHigh, OUTPUT);
  pinMode(pirPin, INPUT);  //last button beneath the file bar (looks like a box with an antenae)
  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
    // don't do anything more:
    return;
  }
  Serial.println("card initialized.");
  bmp.begin();
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.print("hello, world!");
  
  Serial.print("calibrating sensor ");
    for(int i = 0; i < calibrationTime; i++){
      Serial.print(".");
      delay(1000);
      }
    Serial.println(" done");
    Serial.println("SENSOR ACTIVE");
    delay(50);
  

}
 
void loop()                     // run over and over again
{
 // get values 
 float temperature = getVoltage(temperaturePin);  //getting the voltage reading from the temperature sensor
 temperature = (temperature - .5) * 100;          //converting from 10 mv per degree wit 500 mV offset
                                                  //to degrees ((volatge - 500mV) times 100)
 float light = getVoltageLight(lightPin);
 float tmpBPM085 = bmp.readTemperature();
 float pressure = bmp.readPressure();
 
 // print some stuff to serial
 Serial.print(temperature); //printing the result
 Serial.println(" degrees Celsius");
 Serial.print(light); //printing the result
 Serial.println(" light intensity");
 
 // set led, make red when difference > 0.5 degree
 if(digitalRead(pirPin) == HIGH){
   digitalWrite(ledPinHigh,HIGH);
   
 Serial.println("motion detected!");
 }
 else {
    digitalWrite(ledPinHigh,LOW);
 //   digitalWrite(ledPinLow,HIGH);
   Serial.println("no motion detected...");
 }
 
 // open the file to write on SD
 File dataFile = SD.open("datalog.txt", FILE_WRITE);

  // if the file is available, write to it:
  if (dataFile) {
    dataFile.print(temperature);
    dataFile.print("  ");
    dataFile.print(tmpBPM085);
    dataFile.print("  ");
    dataFile.print(pressure);
    dataFile.print("  ");
    dataFile.println(light);
    dataFile.close();
    // print to the serial port too:
    //Serial.println(temperature);
  }  
  // if the file isn't open, pop up an error:
  else {
    Serial.println("error opening datalog.txt");
  }
  // print stuff to lcd
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(temperature);
  lcd.print(" = ");
  lcd.print(tmpBPM085);
  lcd.setCursor(0, 1);
  lcd.print(round(pressure));
  lcd.print(" = ");
  lcd.print(round(light));
  
  // print more stuff to serial
  Serial.print("Temperature BMP085 = ");
  Serial.print(bmp.readTemperature());
  Serial.println(" *C");
 
  Serial.print("Pressure = ");
  Serial.print(bmp.readPressure());
  Serial.println(" Pa");
  Serial.print("Altitude = ");
  Serial.print(bmp.readAltitude());
  Serial.println(" meters");
  Serial.println();
  
  delay(10000);                                     //waiting a second or more
}

/*
 * getVoltage() - returns the voltage on the analog input defined by
 * pin
 */
float getVoltage(int pin){
 return (analogRead(pin) * .004882814); //converting from a 0 to 1023 digital range
                                        // to 0 to 5 volts (each 1 reading equals ~ 5 millivolts
}
float getVoltageLight(int pin){
 return (analogRead(pin)); //converting from a 0 to 1023 digital range
                                        // to 0 to 5 volts (each 1 reading equals ~ 5 millivolts
}

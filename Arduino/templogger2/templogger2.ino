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

//TMP36 Pin Variables
int temperaturePin = 0; //the analog pin the TMP36's Vout (sense) pin is connected to
                        //the resolution is 10 mV / degree centigrade 
                        //(500 mV offset) to make negative temperatures an option
int lightPin = 1;
int ledPinHigh = 3;
int ledPinLow = 2;
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
  pinMode(ledPinLow, OUTPUT);  //last button beneath the file bar (looks like a box with an antenae)
  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
    // don't do anything more:
    return;
  }
  Serial.println("card initialized.");
  bmp.begin();
}
 
void loop()                     // run over and over again
{
 float temperature = getVoltage(temperaturePin);  //getting the voltage reading from the temperature sensor
 temperature = (temperature - .5) * 100;          //converting from 10 mv per degree wit 500 mV offset
                                                  //to degrees ((volatge - 500mV) times 100)
 float light = getVoltageLight(lightPin);
 float tmpBPM085 = bmp.readTemperature();
 float pressure = bmp.readPressure();
 Serial.print(temperature); //printing the result
 Serial.println(" degrees Celsius");
 Serial.print(light); //printing the result
 Serial.println(" light intensity");
 if (abs (temperature - tmpBPM085)>0.5){
   digitalWrite(ledPinHigh,HIGH);
   digitalWrite(ledPinLow,LOW);
 //  Serial.println(" temp high");
 }
 else {
    digitalWrite(ledPinHigh,LOW);
    digitalWrite(ledPinLow,HIGH);
  //  Serial.println(" temp low");
 }
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
  // read stuff from BMP085
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
 delay(10000);                                     //waiting a second
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

// https://github.com/PaulStoffregen/Time
#include <TimeLib.h>

int sensorPin = 5;
int lightVal;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  setTime(0);
}

void loop() {
  // put your main code here, to run repeatedly:
  lightVal = analogRead(sensorPin);
  if (lightVal >= 40) {
    printTimeStamp("Activated => Start: ");
    unsigned long start = millis();
    while (lightVal >= 40) {
      lightVal = analogRead(sensorPin);
      delay(10);
    }
    unsigned long diff = millis()-start;
    printTimeStamp(", End: ");
    Serial.print(" => Milliseconds Elapsed: ");
    Serial.println(diff);
  }
  
  delay(200);
}

void printTimeStamp(const char* status) {
  Serial.print(status);
  Serial.print(hour());
  Serial.print(":");
  Serial.print(minute());
  Serial.print(":");
  Serial.print(second());
}

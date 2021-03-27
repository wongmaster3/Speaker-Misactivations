// https://github.com/PaulStoffregen/Time
#include <TimeLib.h>

int sensorPin = 5;
int lightVal;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
//  Serial.println(now());
}

void loop() {
  // put your main code here, to run repeatedly:
  lightVal = analogRead(sensorPin);
  if (lightVal >= 10) {
    Serial.println("Activated =>");
    Serial.println("Start: " + now());
    unsigned long start = millis();
    while (lightVal >= 10) {
      lightVal = analogRead(sensorPin);
    }
    unsigned long diff = millis()-start;
    Serial.println("End: " + now());
    Serial.println("Milliseconds Elapsed: " + diff);
  }
  delay(200);
}

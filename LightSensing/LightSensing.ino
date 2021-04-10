#define ON 1
#define OFF 0

int sensorPin = 5;
int lightVal;
int threshold;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  threshold = analogRead(sensorPin)+10;
}

void loop() {
  // put your main code here, to run repeatedly:
  lightVal = analogRead(sensorPin);
  if (lightVal >= threshold) {
    Serial.println(ON);

    unsigned long start = millis();
    while (lightVal >= threshold) {
      lightVal = analogRead(sensorPin);
      delay(5);
    }

    Serial.println(OFF);
  }

  delay(200);
}

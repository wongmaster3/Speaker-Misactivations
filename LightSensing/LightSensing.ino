#define ON 1
#define OFF 0

int sensorPin = A5;
int lightVal;
int threshold;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  threshold = analogRead(sensorPin)+6;
}

void loop() {
  // put your main code here, to run repeatedly:
  lightVal = analogRead(sensorPin);
  if (lightVal >= threshold) {
    Serial.println(ON);

    while (lightVal >= threshold) {
      lightVal = analogRead(sensorPin);
      delay(75);
    }

    Serial.println(OFF);
  }

  delay(10);
}

#define ON 1
#define OFF 0

int sensorPin = A5;
float lightVal;
float threshold;

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
      lightVal = sample();
    }

    Serial.println(OFF);
  }

  delay(10);
}

float sample() {
  float maximum = -1.0;
  int samples = 4;
  for (int i = 0; i < samples; i++) {
    int currentVal = analogRead(sensorPin);
    maximum = (maximum < currentVal) ? currentVal : maximum;
    delay(20);
  }
  return maximum;
}

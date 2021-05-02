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
  float total = 0;
  int samples = 4;
  for (int i = 0; i < samples; i++) {
    total += analogRead(sensorPin);
    delay(20);
  }
  return total/samples;
}

#define ON 1
#define OFF 0

int sensorPin = 5;
int lightVal;
int threshold = 40;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
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
    
    unsigned long diff = millis()-start;
    Serial.println(OFF);
    Serial.println(diff);
  }
  
  delay(200);
}

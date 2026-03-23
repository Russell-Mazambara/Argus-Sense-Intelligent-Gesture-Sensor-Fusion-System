//Fully Funtional
const int trigPin = 9;
const int echoPin = 10;
const int lightSensor1 = A0;
const int lightSensor2 = A1;

long duration;
int distance;

bool isValidDistance(int dist) {
  return ((dist >= 2) && (dist <= 400));}

bool isValidLightReading(int value) {
 return ((value >= 0) && (value <= 1023)); }

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.println("Sensor test starting...");
}

void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);  

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;

  int light1Value = analogRead(lightSensor1);
  int light2Value = analogRead(lightSensor2);

  if (isValidDistance(distance) && 
      isValidLightReading(light1Value) && 
      isValidLightReading(light2Value)) {
    Serial.print("US:");
    Serial.print(distance);
    Serial.print(",L1:");
    Serial.print(light1Value);
    Serial.print(",L2:");
    Serial.println(light2Value);
  }

  delay(100);
}
const int trigPin = 9;
const int echoPin = 10;
const int lightSensor1 = A0;
const int lightSensor2 = A1;

// NEW: RGB LED pins
const int redPin = 5;
const int greenPin = 6;
const int bluePin = 3;

long duration;
int distance;

bool isValidDistance(int dist)
{
  return (dist >= 2 && dist <= 400);
}

bool isValidLightReading(int value)
{
  return (value >= 0 && value <= 1023);
}

void setup()
{
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // NEW: Set up LED pins
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);

  // Start with LED off
  setLED(0, 0, 0);

  Serial.println("Sensor test starting...");
}

// NEW: Function to set LED color
void setLED(int r, int g, int b) {
  // INVERT the values for common anode LED
  analogWrite(redPin, 255 - r);    // Inverted!
  analogWrite(greenPin, 255 - g);  // Inverted!
  analogWrite(bluePin, 255 - b);   // Inverted!
}

void loop()
{
  // Check for incoming commands from Python
  if (Serial.available() > 0)
  {
    String command = Serial.readStringUntil('\n');
    command.trim();

    // Parse LED command format: "LED:R,G,B"
    if (command.startsWith("LED:"))
    {
      command.remove(0, 4); // Remove "LED:" prefix

      int r = command.substring(0, command.indexOf(',')).toInt();
      command.remove(0, command.indexOf(',') + 1);

      int g = command.substring(0, command.indexOf(',')).toInt();
      command.remove(0, command.indexOf(',') + 1);

      int b = command.toInt();

      setLED(r, g, b);
    }
  }

  // Read ultrasonic sensor
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;

  // Read light sensors
  int light1Value = analogRead(lightSensor1);
  int light2Value = analogRead(lightSensor2);

  // Send sensor data if valid
  if (isValidDistance(distance) &&
      isValidLightReading(light1Value) &&
      isValidLightReading(light2Value))
  {
    Serial.print("US:");
    Serial.print(distance);
    Serial.print(",L1:");
    Serial.print(light1Value);
    Serial.print(",L2:");
    Serial.println(light2Value);
  }

  delay(100);
}
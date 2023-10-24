#define trigPin1 2
#define echoPin1 7
#define trigPin2 3
#define echoPin2 8

void setup() {
  Serial.begin(9600);
  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin1, INPUT);
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);
}

void loop() {
  float distance1 = getDistance(trigPin1, echoPin1);
  float distance2 = getDistance(trigPin2, echoPin2);

  Serial.print("Sensor 1: ");
  Serial.print(distance1);
  Serial.println(" cm");
  
  Serial.print("Sensor 2: ");
  Serial.print(distance2);
  Serial.println(" cm");

  delay(1000); // 1초마다 센서 값을 측정
}

float getDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  float duration = pulseIn(echoPin, HIGH);
  float distance = (duration / 2) * 0.0343; // 소리의 속도 (약 343 m/s)
  return distance;
}

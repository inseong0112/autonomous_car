#define LED_R 13
#define LED_Y 12
#define LED_G 11
 
void setup() {
  // put your setup code here, to run once:
  pinMode(LED_R, OUTPUT);
  pinMode(LED_Y, OUTPUT);
  pinMode(LED_G, OUTPUT);
}
 
void loop() {
  // put your main code here, to run repeatedly:
  
  digitalWrite(LED_R, HIGH);
  delay(2000);
  digitalWrite(LED_R, LOW);
 
  //digitalWrite(LED_Y, HIGH);
  delay(1000);

 
  digitalWrite(LED_G, HIGH);
  delay(2000);
  digitalWrite(LED_G, LOW);

}
 
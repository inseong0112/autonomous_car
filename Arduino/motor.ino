//a1~d2 핀 연결, - 왼쪽(파란색) -> 5V, 오른쪽(빨간색) -> GND

int a1 = 5;
int a2 = 6;
int b1 = 7;
int b2 = 8;
int c1 = 9;
int c2 = 10; 
int d1 = 11;
int d2 = 12;

void setup() {

  pinMode(a1, OUTPUT);              // 5번핀을 출력모드로 설정합니다.

  pinMode(a2, OUTPUT);              // 6번핀을 출력모드로 설정합니다.

  pinMode(b1, OUTPUT);             // 10번핀을 출력모드로 설정합니다.

  pinMode(b2, OUTPUT);           // 11번핀을 출력모드로 설정합니다.

  pinMode(c1, OUTPUT);             // 10번핀을 출력모드로 설정합니다.

  pinMode(c2, OUTPUT);           // 11번핀을 출력모드로 설정합니다.
  
  pinMode(d1, OUTPUT);             // 10번핀을 출력모드로 설정합니다.

  pinMode(d2, OUTPUT);           // 11번핀을 출력모드로 설정합니다.

}

void loop() {

digitalWrite(a1, HIGH);
digitalWrite(a2, LOW);
digitalWrite(b1, HIGH);
digitalWrite(b2, LOW);
digitalWrite(c1, HIGH);
digitalWrite(c2, LOW);
digitalWrite(d1, HIGH);
digitalWrite(d2, LOW);
delay(100);

}
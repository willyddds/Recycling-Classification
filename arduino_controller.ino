#include <Servo.h>
Servo myservo[3];         //三軸
const  byte servo_pin[3]={7,A1,A0};//0==底
const int sensorPin = A4;//FSR

void controlServo(int value) {
  Serial.println("MOVING"); // 告知樹莓派手臂開始動作
  Catch();
  delay(1000);
  if (value == 0){           //metal
    if(fsr()==1){            //iron
      myservo[0].write(100);
    }
    else{                    //ALU
      myservo[0].write(120);
    }
  } 
  else if (value == 1){     //pg
    if(fsr()==1){           //glass
      myservo[0].write(140);
    }
    else{                   //plastic
      myservo[0].write(160);
    }
  } 
  else { //paper
    myservo[0].write(180);
  } 
  delay(1000);
  drop();

  Serial.println("Finish"); // 告知樹莓派手臂動作完成
} 

void Catch(){
  reset();
  delay(1000);
  myservo[1].write(90);
  delay(700);
  myservo[2].write(80);
  delay(700);
  myservo[1].write(40);
  delay(500);
}

void drop(){
  delay(1000);
  myservo[1].write(90);
  delay(500);
  myservo[2].write(0);
  delay(500);
  myservo[1].write(40);
}

void setup() {
  reset();
  pinMode(sensorPin, INPUT); // 設定傳感器引腳為輸入模式
  Serial.begin(9600);
  for(byte i = 0; i < 3; i++ ){ 
        myservo[i].attach(servo_pin[i]); 
  }
}

void reset(){
  myservo[2].write(0);
  myservo[1].write(40);
  delay(500);
  myservo[0].write(0);
  delay(1000);
}

int fsr(){
  int sensorState = digitalRead(sensorPin); // 讀取傳感器狀態
  return sensorState;
}

void loop() {
  if (Serial.available() > 0) {
    int receivedValue = Serial.parseInt();  // 讀取從樹莓派接收的數字
    if(receivedValue>=0 && receivedValue<=2){
      controlServo(receivedValue);  // 控制伺服馬達
    }
  }
}

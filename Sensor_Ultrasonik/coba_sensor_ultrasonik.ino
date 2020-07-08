//PWM = 3, 5, 6, 9, 10, 11
//Non-PWM = 0, 1, 2, 4, 7, 8, 12, 13

//Sensor pins (echo & trigger)
#define trigPin1 2
#define echoPin1 3
#define trigPin2 4
#define echoPin2 5
#define trigPin3 6
#define echoPin3 7
//#define trigPin4 8
//#define echoPin4 9

//Pins for raspberry pi
#define us_1 10
#define us_2 11
#define us_3 12
//#define us_4 13

long duration, distance, Sensor1,Sensor2,Sensor3,Sensor4,Sensor5,Sensor6;

void setup()
{
Serial.begin (9600);
pinMode(trigPin1, OUTPUT);
pinMode(trigPin2, OUTPUT);
pinMode(trigPin3, OUTPUT);
//pinMode(trigPin4, OUTPUT);

pinMode(echoPin1, INPUT);
pinMode(echoPin2, INPUT);
pinMode(echoPin3, INPUT);
//pinMode(echoPin4, INPUT);

pinMode(us_1, OUTPUT);
pinMode(us_2, OUTPUT);
pinMode(us_3, OUTPUT);
//pinMode(us_4, OUTPUT);

}

void loop() {
SonarSensor(trigPin1, echoPin1);
Sensor1 = distance;
kirim(Sensor1, us_1);

//SonarSensor(trigPin2, echoPin2);
Sensor2 = distance;
kirim(Sensor2, us_2);

//SonarSensor(trigPin3, echoPin3);
Sensor3 = distance;
kirim(Sensor3, us_3);

//SonarSensor(trigPin4, echoPin4);
//Sensor4 = distance;
//kirim(Sensor4, us_4);

Serial.print(Sensor1);
Serial.print(" - ");
Serial.print(Sensor2);
Serial.print(" - ");
Serial.println(Sensor3);
//Serial.print(" - ");
//Serial.println(Sensor4);
}

void SonarSensor(int trigPin,int echoPin)
{
digitalWrite(trigPin, LOW);
delayMicroseconds(1);
digitalWrite(trigPin, HIGH);
delayMicroseconds(5);
digitalWrite(trigPin, LOW);
duration = pulseIn(echoPin, HIGH);
distance = (duration/2) / 29.1;
}

//kirim status ke raspberry pi
void kirim(int sensor,int us_pin){
  if(sensor <= 30){
    digitalWrite(us_pin, HIGH);
  }
  if(sensor > 30){
    digitalWrite(us_pin, LOW);
  }
}

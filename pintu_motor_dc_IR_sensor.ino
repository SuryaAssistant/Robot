/*
 * Program untuk buka pintu (gagang pintu = off)
 * 
 * Membaca dari sensor infrared
 * Infrared = on, maka pintu membuka, tunggu x detik, tutup
 * Motor DC tanpa encoder
 * Motor driver: IBT-2
 */

//#include <Arduino.h>
#define SENSOR_IR 2
#define RPWM_out 5 //connect to IBT-2, pin 1 (RPWM)
#define LPWM_out 6 //connect to IBT-2, pin 2 (LPWM)

int posisi_pintu = 0;
int IR_status_a;
int IR_status_b;
int IR_status_c;
int IR_status = 0; //0 = diam, 1 = buka, 2 = tunggu, 3 = tutup
 
void pintu()
{
  IR_status = digitalRead(SENSOR_IR);
  Serial.print("IR = ");
  Serial.println(IR_status);
}

void setup() 
{
  pinMode(RPWM_out, OUTPUT);
  pinMode(LPWM_out, OUTPUT);
  //attachInterrupt(digitalPinToInterrupt(2),pintu,FALLING);
  pinMode(SENSOR_IR, INPUT);
  int posisi_pintu = 0; // 0 = diam, 1 = buka, 2 = tunggu, 3 = tutup
  Serial.begin(9600);
}


void loop() 
{
  int IR_Value = digitalRead(SENSOR_IR);
  
  if (IR_Value == LOW)
  {
    IR_status_a = digitalRead(SENSOR_IR);
    if (IR_status_a - 0 == 0)
    {
      IR_status = 1;
    }
    else
    {
      IR_status = 0;
    }
    
    cek_pintu:
    Serial.print("IR = ");
    Serial.print(IR_status);
    if(IR_status == 1)
    {
      if (posisi_pintu == 0)
      {      
        motor_buka();
        delay(3000);
        posisi_pintu = 1;
        goto cek_pintu;
      }
      
      if (posisi_pintu == 1)
      { 
        tunggu:
        motor_tunggu();
        IR_status_b = digitalRead(SENSOR_IR);
        delay(3000);
        if (IR_status - IR_status_b != 0)
        {
         Serial.print("IRb = ");
         Serial.print(IR_status_b);
         Serial.println("\t tunggu dulu");
         goto tunggu;
        }
        else
        {
         posisi_pintu = 2;
        }
        IR_status_b = 1;
        goto cek_pintu;
      }
      
      if (posisi_pintu == 2)
      { 
        mau_tutup:
        Serial.println("\t Pintu mau ditutup");
        IR_status_c = digitalRead(SENSOR_IR);
        delay(3000);
        if (IR_status - IR_status_c != 0)
        {
         Serial.print("IRc = ");
         Serial.print(IR_status_c);
         Serial.println("\t tunggu dulu");
         goto mau_tutup;
        }
        else
        {
          motor_tutup();
          delay(3000);
        }
        posisi_pintu = 0;
        IR_status_c = 1;
      }
    }
  }
  
  if (IR_Value == HIGH)
  {
    motor_diam();
  }
  
  akhir:
  delay(500);
}

/*
 * Fungsi buka_tutup_stop motor
 */
 
void motor_diam()
{
  analogWrite(LPWM_out, 0);
  analogWrite(RPWM_out, 0);
  int posisi_pintu = 0;
  Serial.println("\t Pintu tutup");
}

void motor_buka()
{
  analogWrite(LPWM_out, 0);
  analogWrite(RPWM_out, 255);
  int posisi_pintu = 1;
  Serial.println("\t Pintu membuka");
}

void motor_tunggu()
{
  analogWrite(LPWM_out, 0);
  analogWrite(RPWM_out, 0);
  int posisi_pintu = 2;
  Serial.println("\t Pintu terbuka");
}

void motor_tutup()
{
  analogWrite(LPWM_out, 255);
  analogWrite(RPWM_out, 0);
  int posisi_pintu = 3;
  Serial.println("\t Pintu sedang menutup");
}

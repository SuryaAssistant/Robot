/*
 * Program untuk buka pintu (gagang pintu = off)
 * 
 * Membaca dari sensor infrared
 * Infrared = on, maka pintu membuka, tunggu x detik, tutup
 * Motor Stepper
 * Motor driver: ???
 */


/* kabel Motor Stepper
 *  
 * Kabel Merah OUT 1
 * Kabel Biru OUT 2
 * Kabel Hijau OUT 3
 * Kabel Hitam OUT 4
 */
 
#include <Arduino.h>
#include <Stepper.h>

#define SENSOR_IR D7

// Jumlah step per rotasi
const int stepsPerRevolution = 200;
// Create Instance of Stepper library
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);



//*************Pengaturan Putaran Motor**************



// Menentukan keliling ban
const int radius_ban = 0; //nilai diubah
const int keliling_ban = 2*22/7*radius_ban;
// Mengukur panjang lintasan ban
const int lebar_pintu = 0;  //nilai diubah
const int panjang_lintasan = 2*22/7*lebar_pintu*0.25;
// Menentukan banyak step untuk gerak buka pintu 90 derajat
const int buka_90 = (panjang_lintasan/keliling_ban)*stepsPerRevolution;
// max step = .....?
// Menentukan banyak step untuk gerak tutup pintu 90 derajat
const int tutup_90 = -buka_90;
// Posisi diam
const int  meneng = 0;

// Menghitung step
int stepCount = 0;



//*****************Pengaturan Flag*******************



// Status posisi pintu
int posisi_pintu = 0;
int IR_status_a;
int IR_status_b;
int IR_status_c;

// status keadaan
int IR_status = 0; //0 = diam, 1 = buka, 2 = tunggu, 3 = tutup

// Status sensor
int Sensor_status = LOW;

/*
// Fungsi untuk membaca sensor unutuk status pintu
void pintu_status()
{
  IR_status = digitalRead(SENSOR_IR);
  Serial.print("IR = ");
  Serial.println(IR_status);
}
*/



//*****************Pengaturan Awal*******************



void setup()
{
  // Mengatur kecepatan 60 rpm:
  myStepper.setSpeed(60);
  
  // serial port:
  Serial.begin(9600);
  // pin sensor sebagai input
  pinMode(SENSOR_IR, INPUT);
  int posisi_pintu = 0; // 0 = diam, 1 = buka, 2 = tunggu, 3 = tutup
}



//*****************Pengaturan Gerak******************



void loop() 
{
  // Baca sensor IR
  int IR_Value = digitalRead(SENSOR_IR);

  
  //*****************Objek Didetaksi******************

  
  if (IR_Value == Sensor_status)
  {
    // Membaca sensor sekali lagi untuk mendapat nilai keadaan sensor
    IR_status_a = digitalRead(SENSOR_IR);
    if (IR_status_a == Sensor_status)
    {
      IR_status = 1; //menyatakan ada objek
    }
    
    else
    {
      IR_status = 0; //menyatakan tidak ada objek
    }

    // Checkpoint cek posisi pintu
    cek_pintu:
    Serial.print("IR = ");
    Serial.println(IR_status);

    // Apabila ada objek di depan sensor
    if(IR_status == 1)
    {
      // Apabila dalam keadaan pintu tertutup ada objek, buka pintu
      if (posisi_pintu == 0)
      {      
        motor_buka();
        delay(3000);
        posisi_pintu = 1; //pintu dalam keadaan terbuka
        goto cek_pintu;   //kembali mengecek status sensor
      }

      //Apabila pintu dalam keadaan terbuka dan ada objek, pintu tetap terbuka
      if (posisi_pintu == 1)
      { 
        // checkpoint tunggu (pintu = terbuka, motor = diam)
        tunggu:
        motor_tunggu(); //motor diam
        // mengecek status sensor ; Ada objek = 0; tidak ada objek = 1;
        IR_status_b = digitalRead(SENSOR_IR);
        delay(3000);
        // Apabila sensor mendeteksi objek, maka motor diam lagi
        if (IR_status_b == Sensor_status)
        {
         Serial.print("IRb = ");
         Serial.print(IR_status_b);
         Serial.println("\t tunggu dulu");
         goto tunggu;
        }
        // Apabila tida terdeteksi objek lagi
        else
        {
         posisi_pintu = 2; // pintu kondisi akan menutup
        }
        
        // cek posisi pintu kembali
        goto cek_pintu;
      }

      // Apabila pintu dalam keadaan akan menutup dan ada objek
      if (posisi_pintu == 2)
      { 
        // checkpoint loop
        mau_tutup:
        Serial.println("\t Pintu mau ditutup");
        IR_status_c = digitalRead(SENSOR_IR);
        delay(3000);

        // Apabila ada objek
        if (IR_status_c == Sensor_status)
        {
         Serial.print("IRc = ");
         Serial.print(IR_status_c);
         Serial.println("\t tunggu dulu");
         // kembali looping
         goto mau_tutup;
        }
        // Apabila tidak ada objek, pintu menutup
        else
        {
          motor_tutup();
          delay(3000);
        }
        posisi_pintu = 0; // pintu tertutup
      }
    }
  }



  //*****************Objek Tidak Didetaksi******************

  if (IR_Value != Sensor_status)
  {
    motor_diam();
  }
  
  akhir:
  delay(500);
}



//*********************Function**********************
//*****************Buka_Tutup_Pintu******************



void motor_diam()
{
  myStepper.step(meneng);
  int posisi_pintu = 0;
  Serial.println("\t Pintu tutup");
}

void motor_buka()
{
  myStepper.step(buka_90);
  int posisi_pintu = 1;
  Serial.println("\t Pintu membuka");
}

void motor_tunggu()
{
  myStepper.step(meneng);
  int posisi_pintu = 2;
  Serial.println("\t Pintu terbuka");
}

void motor_tutup()
{
  myStepper.step(tutup_90);
  int posisi_pintu = 3;
  Serial.println("\t Pintu sedang menutup");
}

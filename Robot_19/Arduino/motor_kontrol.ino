//PWM = 3, 5, 6, 9, 10, 11 ; 5&6
//Non-PWM = 0, 1, 2, 4, 7, 8, 12, 13

//R_EN and L_EN using the same pin

//pin D7 use for receiving signal from us_modul to
//stopping motor automatically
#define auto_stop 7

//Motor Depan
#define dpn_RPWM 3 
#define dpn_EN 4 
#define dpn_LPWM 5 

//Motor Belakang
#define blkg_RPWM 6 
#define blkg_EN 8 
#define blkg_LPWM 9 

//Input Raspi
#define in_dpn_R 2
#define in_dpn_L 11

#define in_blkg_R 12
#define in_blkg_L 13

int i;

void setup() {
  Serial.begin(9600);
  
  //Setting Mode Pin
  pinMode(dpn_RPWM, OUTPUT);
  pinMode(dpn_EN, OUTPUT);
  pinMode(dpn_LPWM, OUTPUT);

  pinMode(blkg_RPWM, OUTPUT);
  pinMode(blkg_EN, OUTPUT);
  pinMode(blkg_LPWM, OUTPUT);

  pinMode(in_dpn_R, INPUT);
  pinMode(in_dpn_L, INPUT);

  pinMode(in_blkg_R, INPUT);
  pinMode(in_blkg_L, INPUT);

  //Setting awal pin LOW
  digitalWrite(dpn_EN, LOW);
  analogWrite(dpn_RPWM, 0);
  analogWrite(dpn_LPWM,0);
  
  digitalWrite(blkg_EN, LOW);
  analogWrite(blkg_RPWM, 0);
  analogWrite(blkg_LPWM, 0);

  delay(1000);
}

void loop() {
  int status_kanan = digitalRead(in_dpn_R);
  int status_kiri = digitalRead(in_dpn_L);
  int status_maju = digitalRead(in_blkg_R);
  int status_mundur = digitalRead(in_blkg_L);
  int status_auto_stop = digitalRead(auto_stop);
  
  if(status_kanan == HIGH){
    kanan();
  }

  if(status_kiri == HIGH){
    kiri();
  }

  if(status_kanan == LOW && status_kiri == LOW){
    dpn_diam();
  }

  if(status_maju == HIGH){
    maju();
  }

  if(status_mundur == HIGH){
    mundur();
  }

  if(status_maju == LOW && status_mundur == LOW){
    blkg_diam();
  }

  if(status_auto_stop == HIGH){
    blkg_diam();
  }
}

/*
 * Gerakan roda depan -----------------------------------
 */
void kanan(){
  digitalWrite(dpn_EN, HIGH);
  analogWrite(dpn_RPWM, 100);
  analogWrite(dpn_LPWM, 0);
}

void kiri(){
  digitalWrite(dpn_EN, HIGH);
  analogWrite(dpn_RPWM, 0);
  analogWrite(dpn_LPWM, 100);
}

/*
 * Gerakan roda belakang --------------------------------
 */
 
void maju(){
  digitalWrite(blkg_EN, HIGH);
  analogWrite(blkg_RPWM, 40);
  analogWrite(blkg_LPWM, 0);  
}

void mundur(){
  digitalWrite(blkg_EN, HIGH);
  analogWrite(blkg_RPWM, 0);
  analogWrite(blkg_LPWM, 40);
}

/*
 * Stop ----------------------------------------------
 */
 
void dpn_diam(){
  digitalWrite(dpn_EN, LOW);
  analogWrite(dpn_RPWM, 0);
  analogWrite(dpn_LPWM, 0);
}

void blkg_diam(){
  digitalWrite(blkg_EN, LOW);
  analogWrite(blkg_RPWM, 0);
  analogWrite(blkg_LPWM, 0);
}

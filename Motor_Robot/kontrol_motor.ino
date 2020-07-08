//PWM = 3, 5, 6, 9, 10, 11 ; 5&6
//Non-PWM = 0, 1, 2, 4, 7, 8, 12, 13

//Motor Depan
#define dpn_RPWM 3 
#define dpn_R_EN 4 

#define dpn_LPWM 5 
#define dpn_L_EN 7 

//Motor Belakang
#define blkg_RPWM 6 
#define blkg_R_EN 8 

#define blkg_LPWM 9 
#define blkg_L_EN 10 

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
  pinMode(dpn_R_EN, OUTPUT);
  pinMode(dpn_LPWM, OUTPUT);
  pinMode(dpn_L_EN, OUTPUT);

  pinMode(blkg_RPWM, OUTPUT);
  pinMode(blkg_R_EN, OUTPUT);
  pinMode(blkg_LPWM, OUTPUT);
  pinMode(blkg_L_EN, OUTPUT);

  pinMode(in_dpn_R, INPUT);
  pinMode(in_dpn_L, INPUT);

  pinMode(in_blkg_R, INPUT);
  pinMode(in_blkg_L, INPUT);

  //Setting awal pin LOW
  digitalWrite(dpn_R_EN, LOW);
  analogWrite(dpn_RPWM, 0);
  digitalWrite(dpn_L_EN, LOW);
  analogWrite(dpn_LPWM,0);
  
  digitalWrite(blkg_R_EN, LOW);
  analogWrite(blkg_RPWM, 0);
  digitalWrite(blkg_L_EN, LOW);
  analogWrite(blkg_LPWM, 0);

  delay(1000);
}

void loop() {
  int status_kanan = digitalRead(in_dpn_R);
  int status_kiri = digitalRead(in_dpn_L);
  int status_maju = digitalRead(in_blkg_R);
  int status_mundur = digitalRead(in_blkg_L);

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
}

/*
 * Gerakan roda depan -----------------------------------
 */
void kanan(){
  digitalWrite(dpn_R_EN, HIGH);
  digitalWrite(dpn_L_EN, HIGH);
  analogWrite(dpn_RPWM, 90);
  analogWrite(dpn_LPWM, 0);
}

void kiri(){
  digitalWrite(dpn_R_EN, HIGH);
  digitalWrite(dpn_L_EN, HIGH);
  analogWrite(dpn_RPWM, 0);
  analogWrite(dpn_LPWM, 90);
}

/*
 * Gerakan roda belakang --------------------------------
 */
 
void maju(){
  digitalWrite(blkg_R_EN, HIGH);
  digitalWrite(blkg_L_EN, HIGH);
  analogWrite(blkg_RPWM, 45);
  analogWrite(blkg_LPWM, 0);  
}

void mundur(){
  digitalWrite(blkg_R_EN, HIGH);
  digitalWrite(blkg_L_EN, HIGH);
  analogWrite(blkg_RPWM, 0);
  analogWrite(blkg_LPWM, 45);
}

/*
 * Stop ----------------------------------------------
 */
 
void dpn_diam(){
  digitalWrite(dpn_R_EN, LOW);
  digitalWrite(dpn_L_EN, LOW);
  analogWrite(dpn_RPWM, 0);
  analogWrite(dpn_LPWM, 0);
}

void blkg_diam(){
  digitalWrite(blkg_R_EN, LOW);
  digitalWrite(blkg_L_EN, LOW);
  analogWrite(blkg_RPWM, 0);
  analogWrite(blkg_LPWM, 0);
}

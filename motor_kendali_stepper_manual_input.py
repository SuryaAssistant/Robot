import RPi.GPIO as GPIO
from time import sleep
import sys


# Jumlah step per rotasi
stepsPerRevolution = 200

# Jumlah step yang akan ditempuh
step_count= 0

# Variabel tempat posisi motor sekarang
posisi_motor = 0
posisi_derajat = 0.0

# batas putaran motor
sudut_ke_benda = 45
batas_kanan = 200*(sudut_ke_benda/360)
batas_kiri = -200*(sudut_ke_benda/360)

# pin motor
motor_channel = (29, 31, 33, 35)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# defining more than 1 GPIO channel as output
GPIO.setup(motor_channel, GPIO.OUT)

# satu step ke kanan
def kanan():
    GPIO.output(motor_channel, (GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH))
    sleep(0.02) #0.005
    GPIO.output(motor_channel, (GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.LOW))
    sleep(0.02)
    GPIO.output(motor_channel, (GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW))
    sleep(0.02)
    GPIO.output(motor_channel, (GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH))
    sleep(0.02)

# satu step ke kiri    
def kiri():
    GPIO.output(motor_channel, (GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH))
    sleep(0.02)
    GPIO.output(motor_channel, (GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH))
    sleep(0.02)
    GPIO.output(motor_channel, (GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW))
    sleep(0.02)
    GPIO.output(motor_channel, (GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.LOW))
    sleep(0.02)
    
while True:
    motor_direction = input(' select motor direction ')

    if(motor_direction == 'kanan'):
        print('motor belok kanan \n')
        while (posisi_motor < batas_kanan) :
            kanan()
            step_count = batas_kanan-posisi_motor-2
            step_count = step_count+1
            posisi_motor = posisi_motor+1
            posisi_derajat = posisi_derajat +1.8
            print('Step count = ', step_count   , 'lagi')
            print('Posisi motor = step ', posisi_motor)
            print('Posisi sudut = ' , posisi_derajat)
            if (posisi_motor == batas_kanan):
                print('motor menghadap 45 derajat ke kanan\n')
                break
                
    if(motor_direction == 'kiri'):
        print('motor belok kiri \n')
        while(posisi_motor > batas_kiri) :
            kiri()
            step_count = posisi_motor-batas_kiri
            step_count = step_count - 1
            posisi_motor = posisi_motor-1
            posisi_derajat = posisi_derajat -1.8
            print('Step count = ', step_count, 'lagi')
            print('Posisi motor = step ', posisi_motor)
            print('Posisi sudut = ' , posisi_derajat)
            if (posisi_motor == batas_kiri):
                print('motor menghadap 45 derajat ke kiri\n')
                break

    if(motor_direction == 'tengah'):
        while(posisi_motor != 0) :
            if(posisi_motor > 0):
                print('motor menengahkan ke kiri \n')
                kiri()
                step_count = posisi_motor
                step_count = step_count-1
                posisi_motor = posisi_motor-1
                posisi_derajat = posisi_derajat-1.8
                print('Step count = ', step_count, 'lagi')
                print('Posisi motor = step ', posisi_motor)
                print('Posisi sudut = ' , posisi_derajat)
                if (posisi_motor == 0):
                    print('motor menghadap ke tengah\n')
                    break
            
            if(posisi_motor < 0):
                print('motor menengahkan ke kanan \n')
                kanan()
                step_count = 0-posisi_motor-2
                step_count = step_count+1
                posisi_motor = posisi_motor+1
                posisi_derajat = posisi_derajat +1.8
                print('Step count = ', step_count, 'lagi')
                print('Posisi motor = step ', posisi_motor)
                print('Posisi sudut = ' , posisi_derajat)
                if (posisi_motor == 0):
                    print('motor menghadap ke tengah\n')
                    break
            
    else:
        continue
                
    
    
    #elif(motor_direction == 'q'):
        #print('motor stopped')
#GPIO.cleanup()
#sys.exit(0)


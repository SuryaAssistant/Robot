from __future__ import print_function
#for Videostream
import imutils
from imutils.video import VideoStream
from imutils.video import WebcamVideoStream
#for timing and delay
from time import sleep
import time
#for I/O pins
import RPi.GPIO as GPIO
#for numerical and other calculation
import numpy as np
import argparse
#for OpenCV
import cv2
#for serial communication Arduino-Raspberry Pi
import serial
#for call other script in 'background'
import subprocess
from subprocess import Popen, PIPE

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#-----------------------------Pin Config-----------------------------#

#------------------SERVO------------------#
servoPIN = 18
GPIO.setup(servoPIN, GPIO.OUT)
p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(0)
p.ChangeDutyCycle(0)

#---------------Encoder_pins---------------#

print("Loading...")
sleep(1.00)

print("Start")

#------------------------------Function------------------------------#
flag_encoder_kanan = 0
flag_encoder_kiri = 0

# looping siklus counter timing encoder
counter_loop_encoder = 0

# define for calling script
def kanan():
    flag_encoder_kanan = 1
    p_kanan=subprocess.Popen(["python3", "kontrol_motor_kanan.py"], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p_kanan.communicate()
    print(stdout)
    
def kiri():
    flag_encoder_kiri = 1
    p_kiri=subprocess.Popen(["python3", "kontrol_motor_kiri.py"], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p_kiri.communicate()
    print(stdout)

def mundur():
    p_mundur=subprocess.Popen(["python3", "kontrol_motor_mundur.py"], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p_mundur.communicate()
    print(stdout)
    
def maju():
    p_maju=subprocess.Popen(["python3", "kontrol_motor_maju.py"], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p_maju.communicate()
    print(stdout)
    
def diam():
    p_diam=subprocess.Popen(["python3", "kontrol_motor_diam.py"], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p_diam.communicate()
    print(stdout)

def buka_pintu():
    p=subprocess.Popen(["python3", "IR_Transmit.py"], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    print(stdout)

status_x = "diam"
#---------------------------Kode Awal---------------------------#

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
    help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())

# start video stream
vs = WebcamVideoStream(src=1).start()

print("[INFO] starting video stream...")

# waktu bagi kamera untuk melakukan "pemanasan"
sleep(2.0)

status_jalan = "diam"

# warna
aman = (0, 255, 0)
bahaya = (0, 0, 255)
peringatan = (0, 255, 255)

us_d_tengah = aman
us_d_kanan = aman
us_d_kiri = aman

us_b_tengah = aman
us_b_kanan = aman
us_b_kiri = aman

default_num = 10000

us_kiri_dpn = default_num
us_tengah_dpn = default_num
us_kanan_dpn = default_num

us_kiri_blk = default_num
us_tengah_blk = default_num
us_kanan_blk = default_num

encoder_dpn = 0
width_camera_only = 800
#---------------------------Operation Code---------------------------#

# mengitung waktu untuk membaca serial arduino
counter_us_dpn = 0
subprocess.Popen(["python3", "serial_arduino_depan.py"], stdout=PIPE, stderr=PIPE)
subprocess.Popen(["python3", "serial_arduino_belakang.py"], stdout=PIPE, stderr=PIPE)

while(True):
    
    # Membaca kamera
    # mengambil frame
    frame = vs.read()
    
    # resize for real frame (detection)
    frame = imutils.resize(frame, width=400)
    
    # resize from real
    frame_copy = imutils.resize(frame, width = 800)
    camera_only_frame = imutils.resize(frame, width = width_camera_only)

    if counter_us_dpn == 5:
        # call serial_communication
        #default serial (if serial communication has an error)
        with open("data_serial_default.txt", "r",encoding="utf-8") as f:
            data_serial_default = list(map(int, f.readlines()))
            
        # read stored variable value in data_serial_depan.txt
        with open("data_serial_depan.txt", "r",encoding="utf-8") as g:
            data_serial_depan = list(map(int, g.readlines()))
            
        # get variable value from data_serial.txt
        if data_serial_depan[0] != '':
            us_kiri_dpn = data_serial_depan[0]#serial_arduino.us_kiri_dpn#
        if data_serial_depan[0] == '':
            us_kiri_dpn = data_serial_default[0]
        if data_serial_depan[1] != '':
            us_tengah_dpn = data_serial_depan[1]#serial_arduino.us_tengah_dpn
        if data_serial_depan[1] == '':
            us_tengah_dpn = data_serial_default[0]
        if data_serial_depan[2] != '':
            us_kanan_dpn = data_serial_depan[2]#serial_arduino.us_kanan_dpn
        if data_serial_depan[2] == '':
            us_kanan_dpn = data_serial_default[0]
                        
        with open("data_serial_belakang.txt", "r", encoding = "utf-8") as h:
            data_serial_belakang = list(map(int, h.readlines()))
        # get variable value from data_serial.txt
        if data_serial_belakang[0] != '':
            us_kiri_blk = data_serial_belakang[0]#serial_arduino.us_kiri_blk#
        if data_serial_belakang[0] == '':
            us_kiri_blk = data_serial_default[0]
        if data_serial_belakang[1] != '':
            us_tengah_blk = data_serial_belakang[1]#serial_arduino.us_tengah_blk
        if data_serial_belakang[1] == '':
            us_tengah_blk = data_serial_default[0]
        if data_serial_belakang[2] != '':
            us_kanan_blk = data_serial_belakang[2]#serial_arduino.us_kanan_blk
        if data_serial_belakang[2] == '':
            us_kanan_blk = data_serial_default[0]
            
        
        # Kondisi di layar
        # us_depan
        if us_tengah_dpn <= 50:
            us_d_tengah = bahaya
        if us_tengah_dpn > 50:
            us_d_tengah = aman
        if us_kanan_dpn <= 30:
            us_d_kanan = bahaya
        if us_kanan_dpn > 30:
            us_d_kanan = aman
        if us_kiri_dpn <=30:
            us_d_kiri = bahaya
        if us_kiri_dpn > 30:
            us_d_kiri = aman

        # us_belakang
        if us_tengah_blk <= 50:
            us_b_tengah = bahaya
        if us_tengah_blk > 50:
            us_b_tengah = aman
        if us_kanan_blk <= 30:
            us_b_kanan = bahaya
        if us_kanan_blk > 30:
            us_b_kanan = aman
        if us_kiri_blk <=30:
            us_b_kiri = bahaya
        if us_kiri_blk > 30:
            us_b_kiri = aman
        
        if status_x == "maju":
            if us_tengah_dpn <=50 :
                diam()
                mundur()
                diam()
                status_x = "diam"
            
        if status_x == "mundur":
            if us_tengah_blk <=50 :
                diam()
                maju()
                diam()
                status_x = "diam"
            
        counter_us_dpn = 0

    # status_us_depan
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.rectangle(frame_copy,(0, 0),(300, 10),us_d_kiri,20)
    cv2.rectangle(frame_copy,(500, 0),(800, 10),us_d_kanan,20)
    cv2.rectangle(frame_copy,(400-150, 0),(400+150, 20),us_d_tengah,30)
    cv2.putText(frame_copy,'{}'.format(us_kiri_dpn),(50,15), font, 0.6,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame_copy,'{}'.format(us_tengah_dpn),(385,15), font, 0.6,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame_copy,'{}'.format(us_kanan_dpn),(700,15), font, 0.6,(255,255,255),2,cv2.LINE_AA)

    # status_us_belakang
    cv2.rectangle(frame_copy,(0, 590),(300, 600),us_b_kiri,20)
    cv2.rectangle(frame_copy,(500, 590),(800, 600),us_b_kanan,20)
    cv2.rectangle(frame_copy,(400-150, 580),(400+150, 600),us_b_tengah,30)
    cv2.putText(frame_copy,'{}'.format(us_kiri_blk),(50,595), font, 0.6,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame_copy,'{}'.format(us_tengah_blk),(385,585), font, 0.6,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame_copy,'{}'.format(us_kanan_blk),(700,595), font, 0.6,(255,255,255),2,cv2.LINE_AA)
    
    cv2.putText(frame_copy,'Robot {}'.format(status_jalan),(10,50), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    #cv2.putText(frame_copy,'Encoder {}'.format(encoder_dpn),(10,70), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    
    # info tab
    cv2.putText(camera_only_frame,'Q ~ keluar dari program',(10,600-10), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'W ~ maju',(10,600-150), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'S ~ mundur',(10,600 - 130), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'A ~ belok kiri',(10,600 - 110), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'D ~ belok kanan',(10, 600 - 90), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'X ~ berhenti',(10, 600 - 70), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'O ~ kamera kiri',(10, 600 - 50), font, 0.6,(255,255,255),1,cv2.LINE_AA)
    cv2.putText(camera_only_frame,'P ~ kamera kanan',(10, 600 - 30), font, 0.6,(255,255,255),1,cv2.LINE_AA)

    cv2.putText(frame_copy,'{}'.format(counter_us_dpn),(775,50), font, 0.5,(255,255,255),1,cv2.LINE_AA)

    # show image
    # Frame asli
    #cv2.imshow("Frame", frame)
    #cv2.imshow("Copy", frame_copy)
    
    # hanya tangkapan kamera
    cv2.imshow("Kamera", camera_only_frame)
    
    # Pengecilan 2x dari "Frame asli"
    status_frame = imutils.resize(frame_copy, width=400)
    cv2.imshow("Status", status_frame)
    
    # menambah counter
    counter_us_dpn = counter_us_dpn+1

    key = cv2.waitKey(1) & 0xFF
    if key == ord("w"):
        maju()
        status_jalan = "maju"
        status_x = "maju"
    if key == ord("s"):
        mundur()
        status_jalan = "mundur"
        status_x = "mundur"
    if key == ord("d"):
        kanan()                        
    if key == ord("a"):
        kiri()
    if key == ord("x"):
        diam()
        status_jalan = "berhenti"
        status_x = "diam"

    if key == ord("o"):
        p.ChangeDutyCycle(5)
        time.sleep(0.05)
        p.ChangeDutyCycle(0)
        
    if key == ord("p"):
        p.ChangeDutyCycle(10)
        time.sleep(0.05)
        p.ChangeDutyCycle(0)
        
    if key == ord("m"): #buka pintu
        buka_pintu()
                
    if key == ord("q"):
        break

print("[INFO] cleaning up...")
cv2.destroyAllWindows()
vs.stop()
subprocess.Popen(["pkill", "python3"], stdout=PIPE, stderr=PIPE)

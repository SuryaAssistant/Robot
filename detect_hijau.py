'''
Kode khusus mencari Warna Hijau
'''

# import the necessary packages
from __future__ import print_function
from pyimagesearch.shapedetector import ShapeDetector
from collections import deque
import numpy as np
import argparse
import imutils
from imutils.video import VideoStream
import time
import cv2


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
    help="max buffer size")
args = vars(ap.parse_args())
 
# define the lower and upper boundaries of the colors in the HSV color space
lower = (60, 120, 40) 
upper = (80, 255, 255)

# define standard colors for circle around the object
colors = (0,255,0)

pts = deque(maxlen=args["buffer"])
 
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    vs = VideoStream(src=0).start()
    
# otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(args["video"])

# waktu bagi kamera untuk melakukan "pemanasan"
time.sleep(2.0)

# keep looping
while True:
    centers=[]
    # mengambil frame
    frame = vs.read()
    
    # memilih frame antara video dengan raspi camera
    frame = frame[1] if args.get("video", False) else frame
    
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break
 
    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    ratio = frame.shape[0] / float(frame.shape[0])
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    height_low = 75
    width_line = 600
    height_high = 150
    cv2.line(frame, (0, height_low), (width_line, height_low), (255, 255, 255), 2)
    cv2.line(frame, (0, height_high), (width_line, (height_high)), (255, 255, 255), 2)
    
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
                
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    sd = ShapeDetector()
        
    #mendeteksi kontur warna
    for c in cnts:
    # compute the center of the contour, then detect the name of the
    # shape using only the contour
        M = cv2.moments(c)
        cX = int((M["m10"] / M["m00"]) * ratio)
        cY = int((M["m01"] / M["m00"]) * ratio)
            
        if ((cY>=75 and cY<=150) and (cX>=0 and cX<600)):
            shape = sd.detect(c)
                
            # multiply the contour (x, y)-coordinates by the resize ratio,
            # then draw the contours and the name of the shape on the image
            c = c.astype("float")
            c *= ratio
            c = c.astype("int")
            cv2.drawContours(frame, [c], -1, colors,2)
            cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
                #cv2.putText(frame, shape, (cX + 20, cY), cv2.FONT_HERSHEY_SIMPLEX,
                #            0.5, (255, 255, 255), 2)
            cv2.putText(frame, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                
            #pakai line di bawah untuk mengamati semua luasan warna yang dipilih
    #            ((x, y), radius) = cv2.minEnclosingCircle(c)
    #            x,y,w,h = cv2.boundingRect(c)
                
            # only proceed if at least one contour was found
    #        if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
            c = max(cnts, key=cv2.contourArea)
                
                #pakai line di bawah untuk mengamati hanya satu luasan terbesar dari setiap warna
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            x,y,w,h = cv2.boundingRect(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            
                # only proceed if the radius meets a minimum size. Correct this value for your obect's size
            if radius > 10:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    #menampilkan boundary bentuk persegi
                cv2.rectangle(frame,(x,y),(x+w,y+h),colors, 2)
                    #menampilkan boundary bentuk lingkaran
                    #cv2.circle(frame, (int(x), int(y)), int(radius), colors[key], 2)
                    
                    #menampilkan teks
                    #(x+w) dan (y+h) untuk rectangular dan (x-radius) dan (y-radius) untuk circle
                cv2.putText(frame, "color_detected", (int(x+w),int(y+h)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,colors,2)
                    
                    #menampilkan posisi semua object
                cv2.putText(frame, "X = {0} and Y =  {1}".format(int(cX), int(cY)), (cX - 20, cY - 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                    
    #                if (cY>75 and cY<150):
    #                    if len(cnts)>0:
    #                        cv2.putText(frame, "tengah", (cX+20, cY +20),
    #                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                  
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break


# cleanup the camera and close any open windows
#camera.release()
cv2.destroyAllWindows()
vs.stop()


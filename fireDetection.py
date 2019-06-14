# pip3 install opencv-python
import cv2
import numpy as np
import time
temps = time.time()
cap = cv2.VideoCapture(0)
temps = 0

while True:
    _, frame = cap.read()



    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    lower = [18, 50, 50]
    upper = [35, 255, 255]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    mask = cv2.inRange(hsv, lower, upper)

    no_red = cv2.countNonZero(mask)

    if int(no_red) > 2000:

        if time.time() - temps > 1:
            print ('Fire detected')
        temps = time.time()

    output = cv2.bitwise_and(frame, hsv, mask=mask)

    cv2.imshow("Frame", frame)
    cv2.imshow("Red mask", output)

    key = cv2.waitKey(1)

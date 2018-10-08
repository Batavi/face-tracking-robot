import cv2
import sys
import time
import math
from threading import Thread
import nxt.locator
from nxt.motor import *

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)
centerx = 320
centery = 240
currentx = 0
currenty = 0

def movex(b, currentx, distxfactor):
    x = Motor(b, PORT_B)
    if not currentx in range(310,330):
        #t1.start(b, 10, -10)
        #movex(b, 20, -10*distxfactor)
        if currentx > 0:
            x.turn(-20, 100*distxfactor)
            print 'left'
        elif currentx < 0:
            x.turn(20, 100*distxfactor)
            print 'right'
    time.sleep(0.5)
    sys.exit()

def movey(b, currenty, distyfactor):
    y = Motor(b, PORT_A)
    if not currenty in range(230,250):
        #t1.start(b, 10, -10)
        #movex(b, 20, -10*distxfactor)
        if currenty > 0:
            y.turn(-10, 20*distyfactor)
            print 'up', currenty
        elif currenty < 0:
            y.turn(10, 20*distyfactor)
            print 'down', currenty
    time.sleep(0.5)
    sys.exit()
b = nxt.locator.find_one_brick()



while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        currentx = centerx-x-(w/2)
        currenty =  centery-y-(h/2)
        distxfactor = math.sqrt((float(currentx)/float(centerx))**2) + 0.1
        distyfactor = math.sqrt((float(currenty)/float(centery))**2) + 0.1
        #print 'x', distxfactor
        print 'y', distyfactor
        if distxfactor > 0.2:
            turnleft = Thread(target=movex, args = (b, currentx, distxfactor))
            turnleft.start()
        if distyfactor > 0.2:
            turnup = Thread(target=movey, args = (b, currenty, distyfactor))
            turnup.start()
        #while not x in range(currentx-10, currentx+10):

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()

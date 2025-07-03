import cv2
import numpy as np
import HandTrackingModule as htm
import time
import mediapipe as mp
import autopy



#####################################
wCam, hCam = 640, 480
frameR=100 #frame reduction
smoothening=7

######################################


plocX,plocY=0,0
clocX,clocY=0,0


cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

pTime=0
detector=htm.handDetector(maxHands=1)
wScr,hScr = autopy.screen.size()
print(wScr,hScr)

while True:
    #1.Find hand landmarks
    success, img = cap.read()
    img=detector.findHands(img)
    lmList=detector.findPosition(img)

    # 2.Get the tip of the index and middle finger
    if len(lmList)!=0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        #print(x1,y1,x2,y2)

        # 3.Check fingers that are up
        fingers=detector.fingersUp()
        #print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        # 4.Only Index Finger: Moving Mode
        if fingers[1]==1 and fingers[2]==0:
            # 5.Convert Coordinate

            x3=np.interp(x1,(frameR,wCam-frameR),(0,wScr))
            y3=np.interp(y1,(frameR,hCam-frameR),(0,hScr))

            # 6.Smoothen Values
            clocX=plocX+(x3-plocX)/smoothening
            clocY=plocY+(y3-plocY)/smoothening

            # 7.Move Mouse
            autopy.mouse.move(wScr-clocX,clocY)
            cv2.circle(img,(x1,y1),15,(0,0,255),cv2.FILLED)

            plocX,plocY=clocX,clocY


        # 8.Both fingers are Up : Clicking mode
        if fingers[1]==1 and fingers[2]==1:

            # 9.Find distance between fingers
            length,img,cx,cy=detector.findDistance(8,12,img)
            #print(length)
            if length<30:
                # 10.Click mouse if distance short
                cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)
                autopy.mouse.click()



    # 11.Frame Rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    # 12.Display
    cv2.putText(img,f'FPS:{int(fps)}',(20,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)

    cv2.imshow('Image', img)
    cv2.waitKey(1)
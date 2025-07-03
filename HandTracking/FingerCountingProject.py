import cv2
import time
import os


import HandTrackingModule as htm


wCam,hCam=640,480

cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

pTime=0
detector=htm.handDetector(detectionCon=0.7)

tipsIds=[4,8,12,16,20]
while True:

    success,img=cap.read()
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    if len(lmList)!=0:
        fingers = []

        #THUMB
        if lmList[tipsIds[0]][1]>lmList[tipsIds[0]-1][1]:
            fingers.append(1)

        else:
            fingers.append(0)

        #FOR FINGERS
        for id in range(1,5):

            if lmList[tipsIds[id]][2] < lmList[tipsIds[id]-2][2]:
                #print("Index finger open")
                fingers.append(1)
            else:
                fingers.append(0)

        #print(fingers)
        totalFingers=fingers.count(1)
        print(totalFingers)

        cv2.rectangle(img,(20,225),(170,425),(0,255,0),cv2.FILLED)
        cv2.putText(img,f'{totalFingers}',(45,375),cv2.FONT_HERSHEY_PLAIN,7,(0,0,255),20)



    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS:{int(fps)}',(30,60),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3)




    cv2.imshow("Image",img)
    cv2.waitKey(1)


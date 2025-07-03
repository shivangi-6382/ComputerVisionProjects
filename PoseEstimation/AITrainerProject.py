import cv2
import  numpy as np
import time
import PoseModule as pm

cap=cv2.VideoCapture("AI Trainer/t1.mp4")

detector=pm.poseDetector()
count=0
dir=0
pTime=0
bar=650

while True:
    success,img=cap.read()
    img=cv2.resize(img,(400,680))
    detector.findPose(img,draw=False)
    lmList=detector.findPosition(img,draw=False)
    if len(lmList)>0:
        #Arms
        #detector.findAngle(img,12,14,16)
        #detector.findAngle(img,11,13,15)

        #Legs
        angle=detector.findAngle(img, 24, 26, 28)
        #detector.findAngle(img, 23, 25, 27)

        #Waist
        #detector.findAngle(img, 12, 24, 26)
        #detector.findAngle(img, 11, 23, 25)

        per=np.interp(angle,(195,270),(0,100))
        #print(angle,per)

        bar=np.interp(angle,(195,270),(650,190))

        color=(255,0,255)
        #to check count
        if per==100:
            color=(0,255,0)
            if dir==0:
                count+=0.5
                dir=1

        if per==0:
            color=(0,255,0)
            if dir==1:
                count+=0.5
                dir=0

        print(count)
        cv2.rectangle(img, (330, 190), (380, 650), color, 2)
        cv2.rectangle(img, (330, int(bar)), (380, 650), color, cv2.FILLED)

        cv2.putText(img, f'{int(per)}%', (310,175), cv2.FONT_HERSHEY_PLAIN, 2, color, 3)



        #cv2.rectangle(img,(10,450),(190,650),(0,255,0),cv2.FILLED)

        cv2.putText(img,f'{int(count)}',(50,170),cv2.FONT_HERSHEY_PLAIN,5,(255,0,0),3)

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS: {int(fps)}',(30,50),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3)



    cv2.imshow("Image",img)
    cv2.waitKey(1)

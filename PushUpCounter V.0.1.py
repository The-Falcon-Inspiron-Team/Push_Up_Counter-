import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm
import winsound




cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
direction = 0
form = 0
feedback = "Fix Form"




while cap.isOpened():
     
    ret, frame = cap.read()
   




    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('frame', frame)
   
    frame = detector.findPose(frame, False)
    lmList = detector.findPosition(frame, False)


    count_set = 0


    # print(lmList)
    if len(lmList) != 0:
        elbow = detector.findAngle(frame, 11, 13, 15)
        shoulder = detector.findAngle(frame, 13, 11, 23)
        hip = detector.findAngle(frame, 11, 23,25)
       
        #Percentage of success of pushup
        per = np.interp(elbow, (90, 160), (0, 100))
       
        #Bar to show Pushup progress
        bar = np.interp(elbow, (90, 160), (380, 50))


        #Check to ensure right form before starting the program
        if elbow > 160 and shoulder > 40 and hip > 160:
            form = 1
   
        #Check for full range of motion for the pushup
        if form == 1:
            if per == 0:
                if elbow <= 90 and hip > 160:
                    feedback = "Up"
                    if direction == 0:
                        count += 0.5
                        direction = 1
                else:
                    feedback = "Fix Form"
                   
            if per == 100:
                if elbow > 160 and shoulder > 40 and hip > 160:
                    feedback = "Down"
                    if direction == 1:
                        count += 0.5
                        direction = 0
                        winsound.Beep(4400, 250)
                else:
                    feedback = "Fix Form"
                        # form = 0
               
                   
   
        print(count)
       
        #Draw Bar
        if form == 1:
            cv2.rectangle(frame, (580, 50), (600, 380), (0, 255, 0), 3)
            cv2.rectangle(frame, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                        (255, 0, 0), 2)
           




        #Pushup counter
            cv2.rectangle(frame, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                        (255, 0, 0), 5)
           
            #Feedback
            cv2.rectangle(frame, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
            cv2.putText(frame, feedback, (500, 40 ), cv2.FONT_HERSHEY_PLAIN, 2,
                    (0, 255, 0), 2)
             








       
    cv2.imshow('frame', frame)
   
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
       
cap.release()
cv2.destroyAllWindows()




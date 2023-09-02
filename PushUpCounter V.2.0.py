import cv2
import mediapipe as mp
import os
import ctypes

WINDOW_NAME = 'Full Integration'

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
counter = 0
stage = None
create = None
opname = "output.avi"

def findPosition(frame, draw=True):

  lmList = []

  if results.pose_landmarks:

      mp_drawing.draw_landmarks(

         frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

      for id, lm in enumerate(results.pose_landmarks.landmark):

          h, w, c = frame.shape

          cx, cy = int(lm.x * w), int(lm.y * h)

          lmList.append([id, cx, cy])

          #cv2.circle(frame, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

  return lmList

cap = cv2.VideoCapture(0)
# Full screen mode
cv2.namedWindow(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


with mp_pose.Pose(

    min_detection_confidence=0.7,

    min_tracking_confidence=0.7) as pose:

  while cap.isOpened():
 # get Screen Size
    user32 = ctypes.windll.user32
    screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
 
 # read video frame by frame
    ret, frame = cap.read()

    frame = cv2.flip(frame, 1)

    frame_height, frame_width, _ = frame.shape

    scaleWidth = float(screen_width)/float(frame_width)
    scaleHeight = float(screen_height)/float(frame_height)

    if scaleHeight>scaleWidth:
        imgScale = scaleWidth

    else:
        imgScale = scaleHeight

    newX,newY = frame.shape[1]*imgScale, frame.shape[0]*imgScale
    frame = cv2.resize(frame,(int(newX),int(newY)))

 

    # Flip the frame horizontally for a later selfie-view display, and convert

    # the BGR frame to RGB.

    frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)

    # To improve performance, optionally mark the frame as not writeable to

    # pass by reference.

    results = pose.process(frame)

    # Draw the pose annotation on the frame.

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    lmList = findPosition(frame, draw=True)

    if len(lmList) != 0:

      cv2.circle(frame, (lmList[12][1], lmList[12][2]), 20, (0, 0, 255), cv2.FILLED)

      cv2.circle(frame, (lmList[11][1], lmList[11][2]), 20, (0, 0, 255), cv2.FILLED)

      cv2.circle(frame, (lmList[12][1], lmList[12][2]), 20, (0, 0, 255), cv2.FILLED)

      cv2.circle(frame, (lmList[11][1], lmList[11][2]), 20, (0, 0, 255), cv2.FILLED)

      if (lmList[12][2] and lmList[11][2] >= lmList[14][2] and lmList[13][2]):

        cv2.circle(frame, (lmList[12][1], lmList[12][2]), 20, (0, 255, 0), cv2.FILLED)

        cv2.circle(frame, (lmList[11][1], lmList[11][2]), 20, (0, 255, 0), cv2.FILLED)

        stage = "down"

      if (lmList[12][2] and lmList[11][2] <= lmList[14][2] and lmList[13][2]) and stage == "down":

        stage = "up"

        counter += 1

        counter2 = str(int(counter))

        print(counter)

        os.system("echo '" + counter2 + "' | festival --tts")

    text = "{}:{}".format("Push Ups", counter)

    cv2.putText(frame, text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX,

                1, (255, 0, 0), 2)

    #cv2.imshow('MediaPipe Pose', frame)
    cv2.imshow(WINDOW_NAME, frame)

    if create is None:

      fourcc = cv2.VideoWriter_fourcc(*'XVID')

      create = cv2.VideoWriter(opname, fourcc, 30, (frame.shape[1], frame.shape[0]), True)

    create.write(frame)

    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop

    if key == ord("q"):

      break

    # do a bit of cleanup

cv2.destroyAllWindows()
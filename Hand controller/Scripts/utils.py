import cv2
import mediapipe as mp
import numpy as np
import os
import pyautogui
import time
def calibration(cam,r,hands):
    coordinates = []
    pantalla_pts = np.array([[r[0]/4, r[1]/2], [r[0]/2, 3*r[1]/4], [r[0]/2, r[1]/4], [3*r[0]/4, r[1]/2]], dtype=np.float32)
    while len(coordinates) < 4:
        #print("coordinates: ", coordinates)
        ret, frame = cam.read()
       

        frame=cv2.flip(frame,1)
        frame2=frame.copy()
        frame2=cv2.resize(frame,(1920,1080))
        frame=cv2.resize(frame,(1920,1080))
        
        H, W, _ = frame.shape
        resolucion_frame = np.array([[W/4, H/2], [W/2, 3*H/4], [W/2, H/4], [3*W/4, H/2]], dtype=np.float32)
        i=0
        for point in resolucion_frame:
            x = int(point[0])
            y = int(point[1])
            cv2.circle(frame, (x, y), radius=5, color=(0, 255, 0), thickness=2)
            #poner index de cada circulo
            cv2.putText(frame, str(i), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv2.LINE_AA)
            i+=1



        frame_rgb = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for idx, landmark in enumerate(hand_landmarks.landmark):
                    if idx == 4 or idx == 8 or idx == 12:
                        x = int(landmark.x * W)
                        y = int(landmark.y * H)
                        cv2.circle(frame, (x, y), radius=5, color=(255, 0, 0), thickness=2)
            #capturar landmark 12 si se pulsa tecla enter
            if cv2.waitKey(1) == 13:  # 13 es el código ASCII para la tecla Enter
                x = int(hand_landmarks.landmark[12].x * W)
                y = int(hand_landmarks.landmark[12].y * H)
                coordinates.append([x, y])
                        


        cv2.imshow('Calibration', frame)
        cv2.waitKey(1)
    return coordinates,pantalla_pts
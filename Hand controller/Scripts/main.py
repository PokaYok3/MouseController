import cv2
import mediapipe as mp
import numpy as np
import os
import pyautogui
import time
from utils import calibration
pyautogui.FAILSAFE = False

threshold = 0.03  # Adjust the threshold as needed
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.2,
               min_tracking_confidence=0.2)
def click(hand_landmarks, threshold):
    landmark_4 = hand_landmarks.landmark[4]
    landmark_8 = hand_landmarks.landmark[8]
    distance = np.sqrt((landmark_8.x - landmark_4.x)**2 + (landmark_8.y - landmark_4.y)**2)
    #print("distance: ", distance)
    if distance < threshold:
        print("Click")
        pyautogui.click()
        pyautogui.sleep(0.5)


# Obtener la resolución de la pantalla
resolucion = pyautogui.size()
# Imprimir la resolución
print("La resolución de la pantalla es:", resolucion[0])
coordinates,pantallapuntos=calibration(cap,resolucion,hands)

# Convertir las coordenadas a un array de numpy
coordinates = np.array(coordinates, dtype=np.float32)
print("coordinates: ", coordinates)
print("pantallapuntos: ", pantallapuntos)
# Calibrar la cámara
M = cv2.getPerspectiveTransform(coordinates, pantallapuntos)
print("M: ", M)
cv2.destroyAllWindows()
while True:
    ret, frame = cap.read()
    if not ret:
        continue
    frame=cv2.flip(frame,1)
    frame=cv2.resize(frame,(1920,1080))
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        #print("landmarks: ", results.multi_hand_landmarks)
        for hand_landmarks in results.multi_hand_landmarks:
            for idx, landmark in enumerate(hand_landmarks.landmark):
                if idx == 12:
                    x = int(landmark.x * frame.shape[1])
                    y = int(landmark.y * frame.shape[0])
                    #cv2.putText(frame, str(idx), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
                    cv2.circle(frame, (x, y), radius=10, color=(0, 0, 255), thickness=2)
                    #mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    # Move the mouse to the landmark position
                    mouse_x = int(M[0, 0] * x + M[0, 1] * y + M[0, 2])
                    mouse_y = int(M[1, 0] * x + M[1, 1] * y + M[1, 2])
                    pyautogui.moveTo(mouse_x, mouse_y)
        
        click(hand_landmarks, threshold)
    
    cv2.imshow('Hand Tracking', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Close the camera
cap.release()
cv2.destroyAllWindows()
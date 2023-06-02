
import webbrowser
import cv2
import mediapipe as mp
import time
import os
from threading import Thread

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils

hands = mpHands.Hands()

pTime = 0
cTime = 0

# Temp values
hand = {
    'thumb_x': -1000,
    'thumb_y': 10000,

    'finger_x': 100000,
    'finger_y': 1000000,
}


def open_server():
    os.system('python -m http.server 8000')


def change_pic(addr):
    f = open('index.html', 'w')
    f.close()

    with open('index.html', 'w') as f:
        f.write(
            '<style> img {width: auto; max-height: 100%;}\nh1{color:blue; font-size: x-large} </style>\n')
        f.write('<h1> Current state </h1>\n')
        f.write(f'<img src="{addr}" />\n')
        f.write('<meta http-equiv="refresh" content="3">')


server = Thread(target=open_server)
server.start()

webbrowser.open('http://127.0.0.1:8000')

while True:
    success, img = cap.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                if id == 4:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                    hand.update({'thumb_x': cx, 'thumb_y': cy})

                if id == 8:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                    hand.update({'finger_x': cx, 'finger_y': cy})

                if hand.get('thumb_x') - hand.get('finger_x') <= 10 and hand.get('thumb_y') - hand.get('finger_y') <= 40:
                    change_pic(
                        'https://t0.gstatic.com/licensed-image?q=tbn:ANd9GcQkrjYxSfSHeCEA7hkPy8e2JphDsfFHZVKqx-3t37E4XKr-AT7DML8IwtwY0TnZsUcQ')
                else:
                    change_pic(
                        'https://t1.gstatic.com/licensed-image?q=tbn:ANd9GcRRv9ICxXjK-LVFv-lKRId6gB45BFoNCLsZ4dk7bZpYGblPLPG-9aYss0Z0wt2PmWDb')

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()

    fps = 1 / (cTime - pTime)

    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow('Hand Tracking', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

server.join()

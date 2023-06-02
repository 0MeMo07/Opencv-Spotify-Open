#Made By https://github.com/0MeMo07

import cv2
import mediapipe as mp
import webbrowser
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)

spotify_url = 'https://open.spotify.com/'

finger_distance = 0
touch_count = 0
is_touching = False
last_touch_time = time.time()
touch_interval = 2  

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            finger_distance = abs(thumb_tip.x - index_tip.x) + abs(thumb_tip.y - index_tip.y)

            if finger_distance < 0.05:  
                if not is_touching:
                    current_time = time.time()
                    if current_time - last_touch_time > touch_interval:
                        touch_count += 1
                        last_touch_time = current_time
                        if touch_count % 3 == 0:
                            webbrowser.open(spotify_url)
                            touch_count = 0
            else:
                is_touching = False

            for landmark in hand_landmarks.landmark:
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

    cv2.putText(frame, f'Touches: {touch_count}/3', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

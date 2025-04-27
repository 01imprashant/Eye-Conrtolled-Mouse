import cv2
import mediapipe as mp
import pyautogui
import time

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

# To track blink status
blink = False

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape

    if landmark_points:
        landmarks = landmark_points[0].landmark

        # Cursor movement
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
            if id == 1:
                screen_x = screen_w * landmark.x
                screen_y = screen_h * landmark.y
                pyautogui.moveTo(screen_x, screen_y)

        # Detect blink for click
        left_eye = [landmarks[145], landmarks[159]]
        left_y1 = left_eye[0].y
        left_y2 = left_eye[1].y
        eye_distance = left_y1 - left_y2

        # Draw circles
        for landmark in left_eye:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)

        # Detect blink
        if eye_distance < 0.01 and blink == False:
            blink = True
            pyautogui.click()
            print("Clicked!")
            time.sleep(0.2)  # prevent multiple clicks

        elif eye_distance >= 0.01:
            blink = False

    cv2.imshow('Eye Controlled Mouse', frame)
    cv2.waitKey(1)
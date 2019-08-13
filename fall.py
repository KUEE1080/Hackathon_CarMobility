import cv2
import numpy as np
import pygame

cap = cv2.VideoCapture(0)

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('fallaudio.mp3')
pygame.mixer.music.play()

fall = cv2.VideoCapture('fall.mpeg')

while cap.isOpened():
    main_frame_found, main_frame = cap.read()
    resized_frame = cv2.resize(main_frame, (720, 480))

    fall_vid_found, fall_vid = fall.read()

    fall_vid = cv2.resize(fall_vid, (720, 480))
    _resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
    copy_fall_vid = np.copy(fall_vid)
    copy_fall_vid = cv2.cvtColor(copy_fall_vid, cv2.COLOR_BGR2RGB)

    lower_green = np.array([0, 146, 52])
    upper_green = np.array([200, 255, 203])

    # lower_green = np.array([0, 40, 0])
    # upper_green = np.array([80, 255, 125])

    mask = cv2.inRange(copy_fall_vid, lower_green, upper_green)
    masked_fall = np.copy(copy_fall_vid)
    masked_fall[mask != 0] = [0, 0, 0]
    _resized_frame[mask == 0] = [0, 0, 0]
    final_vid = cv2.cvtColor(_resized_frame + masked_fall, cv2.COLOR_RGB2BGR)

    cv2.imshow("Output", final_vid)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
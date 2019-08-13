import cv2
import numpy as np
import pygame

cap = cv2.VideoCapture(0)

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('springaudio.mp3')
pygame.mixer.music.play()

spring = cv2.VideoCapture('spring.mpeg')

while cap.isOpened():
    main_frame_found, main_frame = cap.read()
    resized_frame = cv2.resize(main_frame, (720, 480))

    spring_vid_found, spring_vid = spring.read()

    spring_vid = cv2.resize(spring_vid, (720, 480))
    _resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
    copy_spring_vid = np.copy(spring_vid)
    copy_spring_vid = cv2.cvtColor(copy_spring_vid, cv2.COLOR_BGR2RGB)

    lower_green = np.array([0, 145, 47])
    upper_green = np.array([203, 255, 201])

    # lower_green = np.array([0, 40, 0])
    # upper_green = np.array([80, 255, 125])

    mask = cv2.inRange(copy_spring_vid, lower_green, upper_green)
    masked_spring = np.copy(copy_spring_vid)
    masked_spring[mask != 0] = [0, 0, 0]
    _resized_frame[mask == 0] = [0, 0, 0]
    final_vid = cv2.cvtColor(_resized_frame + masked_spring, cv2.COLOR_RGB2BGR)

    cv2.imshow("Output", final_vid)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
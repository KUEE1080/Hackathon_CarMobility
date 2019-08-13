import cv2
import numpy as np
import pygame

cap = cv2.VideoCapture(0)

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('pikachu_song.mp3')
pygame.mixer.music.play()

pikachu = cv2.VideoCapture('Pikachu Dancing Green Screen.mp4')

while cap.isOpened():
    main_frame_found, main_frame = cap.read()
    resized_frame = cv2.resize(main_frame, (720, 480))

    pika_vid_found, pika_vid = pikachu.read()

    pika_vid = cv2.resize(pika_vid, (720, 480))
    _resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
    copy_pika_vid = np.copy(pika_vid)
    copy_pika_vid = cv2.cvtColor(copy_pika_vid, cv2.COLOR_BGR2RGB)

    lower_green = np.array([0, 100, 0])
    upper_green = np.array([120, 255, 100])

    # lower_green = np.array([0, 40, 0])
    # upper_green = np.array([80, 255, 125])

    mask = cv2.inRange(copy_pika_vid, lower_green, upper_green)
    masked_pika = np.copy(copy_pika_vid)
    masked_pika[mask != 0] = [0, 0, 0]
    _resized_frame[mask == 0] = [0, 0, 0]
    final_vid = cv2.cvtColor(_resized_frame + masked_pika, cv2.COLOR_RGB2BGR)

    cv2.imshow("Output", final_vid)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
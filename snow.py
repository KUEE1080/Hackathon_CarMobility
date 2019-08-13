import cv2
import numpy as np
import pygame

cap = cv2.VideoCapture(0)

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('snowaudio.mp3')
pygame.mixer.music.play()

snow = cv2.VideoCapture('Snow.mpeg')

while cap.isOpened():
    main_frame_found, main_frame = cap.read()
    resized_frame = cv2.resize(main_frame, (720, 480))

    snow_vid_found, snow_vid = snow.read()

    snow_vid = cv2.resize(snow_vid, (720, 480))
    _resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
    copy_snow_vid = np.copy(snow_vid)
    copy_snow_vid = cv2.cvtColor(copy_snow_vid, cv2.COLOR_BGR2RGB)

    lower_green = np.array([48, 140, 0])
    upper_green = np.array([207, 255, 203])

    # lower_green = np.array([0, 40, 0])
    # upper_green = np.array([80, 255, 125])

    mask = cv2.inRange(copy_snow_vid, lower_green, upper_green)
    masked_snow = np.copy(copy_snow_vid)
    masked_snow[mask != 0] = [0, 0, 0]
    _resized_frame[mask == 0] = [0, 0, 0]
    final_vid = cv2.cvtColor(_resized_frame + masked_snow, cv2.COLOR_RGB2BGR)

    cv2.imshow("Output", final_vid)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
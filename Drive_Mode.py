import cv2
import numpy as np
import matplotlib.pyplot as plt

AREA_MIN = 100

cap = cv2.VideoCapture(0)

while cap.isOpened():
    main_frame_found, main_frame = cap.read()
    resized_frame = cv2.resize(main_frame, (720, 480))
    # resized_frame = cv2.bilateralFilter(resized_frame, 9, 75, 75)

    height = resized_frame.shape[0]
    poly_shape = np.array([[(0, height), (720, height), (500, 170), (200, 170)]])  # - version2..?
    roi_mask = np.zeros_like(resized_frame)
    # cv2.imshow('roi_mask', roi_mask)

    cv2.fillPoly(roi_mask, poly_shape, (255, 255, 255))
    roi_masked_result = cv2.bitwise_and(resized_frame, roi_mask)

    hsv = cv2.cvtColor(roi_masked_result, cv2.COLOR_BGR2HSV)

    # 꼬깔콘 색깔을 잡아준다. 실험적으로 얻은 수치며, 애기능 농구장에서 할 경우, 범위 값을 새로 수정해야 한다.
    lower_orange = np.array([0, 51, 255])
    upper_orange = np.array([30, 255, 255])
    # lower_orange = np.array([0, 51, 255])
    # upper_orange = np.array([28, 255, 255])

    mask = cv2.inRange(hsv, lower_orange, upper_orange)
    res = cv2.bitwise_and(resized_frame, resized_frame, mask=mask)

    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(mask, contours[0], -1, (0, 0, 0), 1)

    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask)

    avg_x = 0
    avg_y = 0

    cnt_valid_centroid = 1
    for i in range(nlabels):
        area = stats[i, cv2.CC_STAT_AREA]
        if area > AREA_MIN:
            avg_x += centroids[i, 0]
            avg_y += centroids[i, 1]
            cnt_valid_centroid += 1

    avg_x = int(avg_x / cnt_valid_centroid)
    avg_y = int(avg_y / cnt_valid_centroid)
    cv2.circle(resized_frame, (avg_x, avg_y), 5, (0, 255, 0), 1)

    left_point = []
    right_point = []

    for i in range(nlabels):
        if i == 0:
            # print("catch")
            continue

        area = stats[i, cv2.CC_STAT_AREA]
        center_x = int(centroids[i, 0])
        center_y = int(centroids[i, 1])
        left = stats[i, cv2.CC_STAT_LEFT]
        top = stats[i, cv2.CC_STAT_TOP]
        width = stats[i, cv2.CC_STAT_WIDTH]
        height = stats[i, cv2.CC_STAT_HEIGHT]

        if area > AREA_MIN:  # 얘가 핵심이다!!! 얼마 정도로 넓이를 보정할 것인가
            print(i)
            pt = []
            pt.append(center_x)
            pt.append(center_y)

            if avg_x > centroids[i, 0]:
                left_point.append(pt)
            else:
                right_point.append(pt)

            # drawing other info on the screen
            cv2.rectangle(resized_frame, (left, top), (left + width, top + height), (0, 0, 255), 1)
            cv2.circle(resized_frame, (center_x, center_y), 5, (255, 0, 0), 1)
            cv2.putText(resized_frame, str(i), (left + 20, top + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    if len(left_point) > 1:
        for i in range(len(left_point) - 1):
            _x1 = left_point[i][0]
            _y1 = left_point[i][1]
            _x2 = left_point[i + 1][0]
            _y2 = left_point[i + 1][1]
            cv2.line(resized_frame, (_x1, _y1), (_x2, _y2), (255, 0, 0), 10)
    elif len(left_point) == 1:
        print("only 1 point found!")
    else:
        print("not able to draw shape")

    if len(right_point) > 1:
        for i in range(len(right_point) - 1):
            _x1 = right_point[i][0]
            _y1 = right_point[i][1]
            _x2 = right_point[i + 1][0]
            _y2 = right_point[i + 1][1]
            cv2.line(resized_frame, (_x1, _y1), (_x2, _y2), (255, 0, 0), 10)
    else:
        print("not able to draw lines")
    # final_vid = resized_frame

    # 아두이노 수신 정보 출력 코드
    overlay = resized_frame.copy()
    # output = resized_frame.copy()

    alpha = 0.7  # 도형의 불투명도!
    beta = 1 - alpha

    cv2.rectangle(overlay, (20, 20), (130, 160), (0, 0, 0), -1)
    cv2.putText(overlay, "{} KM".format(0), (300, 400), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 138, 230), 4)
    cv2.putText(overlay, "{} C".format(25), (35, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
    cv2.putText(overlay, "{} %".format(68), (35, 130), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

    cv2.addWeighted(overlay, alpha, resized_frame, 1 - alpha, 0, resized_frame)
    final_vid = resized_frame

    cv2.imshow("Output", final_vid)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


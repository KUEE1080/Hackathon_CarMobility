from threading import Thread
import cv2
import datetime
import serial
import numpy as np
import pygame
import matplotlib.pyplot as plt

global cap

AREA_MIN = 100

PORT = 'COM3'
BaudRate = 9600
timeout = 1

Ard = serial.Serial(PORT, BaudRate)
code_list = []

NUM_BLADE = 0
RPM = 0
SPEED = 0
TEMPERATURE = 0
HUMIDITY = 0

def Decode(k):
    k = k.decode()
    k = str(k)
    return k

def Ardread():
    if Ard.readable():
        LINE = Ard.readline()
        code=Decode(LINE)

        global code_list
        code_list.append(code)
    else : print("읽기 실패 from _Ardread_")

class Class_Serial_Comm(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        while True:
            for i in range(4):
                Ardread()

            code_str = str(code_list)
            code_str = code_str[1:-1]  # 결과들 깔끔하게
            a = code_str.split(', ')  # (,로 split하여 리스트만들기)

            value = []
            for i in range(len(a)):
                if 0 <= i <= 2:
                    a_str = str(a[i])
                    a_list_t = a_str.split('=')
                    k = a_list_t[1]
                    k = k[0:-5]  # k는 숫자값을 string으로 표현한것
                    value.append(int(k))

                elif i == 3:
                    a = str(a[i])
                    a = a.split(' ')
                    tem = a[0]
                    hum = a[1]
                    tem = tem[13:-1]
                    hum = hum[9:-1]
                    tem = int(tem)
                    hum = int(hum)
                    value.append(tem)
                    value.append(hum)

            print(value)
            global NUM_BLADE, RPM, SPEED, TEMPERATURE, HUMIDITY
            NUM_BLADE = value[0]
            RPM = value[1]
            SPEED = str(value[2])
            TEMPERATURE = str(value[3])
            HUMIDITY = str(value[4])

class Class_Main(Thread):
    def __init__(self):
        global cap
        Thread.__init__(self)
        cap = cv2.VideoCapture(0)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            global NUM_BLADE, RPM, SPEED, TEMPERATURE, HUMIDITY
            print("beta")
            main_frame_found, main_frame = cap.read()
            resized_frame = cv2.resize(main_frame, (720, 480))
            # resized_frame = cv2.bilateralFilter(resized_frame, 9, 75, 75)

            height = resized_frame.shape[0]
            poly_shape = np.array([[(0, height), (720, height), (500, 170), (200, 170)]])  # - version2..?
            roi_mask = np.zeros_like(resized_frame)
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

            # 아두이노 수신 정보 출력 코드
            overlay = resized_frame.copy()

            alpha = 0.7  # 도형의 불투명도!

            cv2.rectangle(overlay, (20, 20), (130, 160), (0, 0, 0), -1)
            cv2.putText(overlay, "{} KM".format(SPEED), (300, 400), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 138, 230), 4)
            cv2.putText(overlay, "{} C".format(TEMPERATURE), (35, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
            cv2.putText(overlay, "{} %".format(HUMIDITY), (35, 130), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

            cv2.addWeighted(overlay, alpha, resized_frame, 1 - alpha, 0, resized_frame)
            final_vid = resized_frame

            cv2.imshow("Output", final_vid)
            cv2.waitKey(10)

            # font = cv2.FONT_HERSHEY_SIMPLEX
            # dat = str(datetime.datetime.now())
            # frame = cv2.putText(frame, dat, (74, 68), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            # print("speed: " + str(SPEED))
            # print("temperature: " + str(TEMPERATURE))
            # cv2.imshow('Final_Video', frame)
            # cv2.waitKey(10)

    # cap.release()
    # cv2.destroyAllWindows()


Class_Serial_Comm()
Class_Main()

while True:
    pass
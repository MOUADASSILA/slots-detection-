#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mon May 13 10:24:21 2024 tarihinde oluşturuldu

@author: mac
"""

import cv2
import time

video_path = "/Users/mac/Desktop/parking spot opencv homework/parking.mp4"
cap = cv2.VideoCapture(video_path)
parking_slots = [(402, 239), (753, 377), (55, 100), (56, 146), (51, 241), (53, 290), (51, 192), (405, 189), (402, 138), (405, 90), (514, 92), (511, 139), (514, 187), (512, 236), (163, 99), (164, 147), (158, 194), (159, 243), (161, 290), (55, 337), (162, 339), (160, 388), (162, 429), (52, 431), (53, 479), (163, 479), (168, 525), (165, 576), (165, 620), (56, 623), (51, 573), (52, 527), (402, 289), (402, 338), (404, 382), (405, 427), (405, 526), (403, 569), (406, 619), (512, 524), (512, 568), (513, 620), (511, 426), (511, 380), (513, 329), (511, 284), (751, 88), (751, 136), (750, 188), (753, 232), (753, 276), (751, 327), (757, 427), (753, 472), (757, 518), (760, 573), (760, 616), (901, 620), (901, 576), (892, 141), (892, 190), (893, 235), (894, 284), (897, 330), (898, 375), (901, 424), (903, 474), (899, 522), (46, 385)]
rect_width, rect_height = 100, 33
color = (0,0,255)
thick = 1
threshold = 30
last_call_time = time.time()
prevFreeslots=0

def convert_grayscale(frame):
    # Resmi gri tonlamaya dönüştür
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Bir ikili resim oluşturmak için eşik uygula
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # İkili resimde konturları bul
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Tamam, şimdi giriş resmiyle aynı boyutlarda siyah bir tuval oluştur
    contour_image = frame.copy()
    contour_image[:] = 0  # Siyah ile doldur

    # Beyaz üzerinde siyah tuvale konturları çiz
    cv2.drawContours(contour_image, contours, -1, (255, 255, 255), thickness=2)
    return contour_image

def mark_slots(frame, grayscale_frame):
    global last_call_time
    global prevFreeslots
    current_time = time.time()
    elapsed_time = current_time - last_call_time

    freeslots=0
    for x, y in parking_slots:
        x1=x+10
        x2=x+rect_width-11
        y1=y+4
        y2=y+rect_height
        start_point, stop_point = (x1,y1), (x2, y2)

        crop=grayscale_frame[y1:y2, x1:x2]
        gray_crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

        # Sıfır olmayan piksel sayısını al
        count=cv2.countNonZero(gray_crop)

        # Eşik değerine göre rengi ve kalınlığı ata
        color, thick = [(0,255,0), 5] if count<threshold else [(0,0,255), 2]

        if count<threshold:
            freeslots = freeslots+1
        
        cv2.rectangle(frame, start_point, stop_point, color, thick)

        ## Her park yeri dikdörtgenindeki sıfır olmayan piksel sayısını göstermek için aşağıdakileri açın
        ## text_x = x1+5
        ## text_y = y1 + 10  # Metni dikdörtgenin üstüne yerleştirmek için Y koordinatını ayarlayın
        ## cv2.putText(frame, str(count), (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 255, 255), 1)

    current_time = time.time()
    if current_time - last_call_time >= 0.1:
        cv2.putText(frame, "Bos yerler:" + str(freeslots), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 255, 255), 2)
        last_call_time = current_time
        prevFreeslots = freeslots
    else:
         cv2.putText(frame, "Bos yerler:" + str(prevFreeslots), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 255, 255), 2)
    return frame
    
while True:
        # videoyu kare kare oku
        ret, frame = cap.read()
        if not ret:break
        grayscale_frame = convert_grayscale(frame)
        out_image = mark_slots(frame, grayscale_frame)        
       
        # sonuçları görüntüleme
        cv2.imshow("Park Yeri Tespit Edici", out_image)          
        # çıkış koşulu
        k = cv2.waitKey(1)
        if k & 0xFF == ord('q'):
            break
        
time.sleep(25)

cap.release()
cv2.destroyAllWindows()

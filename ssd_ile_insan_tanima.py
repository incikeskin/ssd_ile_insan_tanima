# ssd_ile_insan_tanima
import cv2
import numpy as np
import os
import time

classes = ["background", "aeroplane", "bicycle", "bird", "boat","bottle","bus","car","cat","chair","cow","diningtable",
          "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

colors = np.random.uniform(0,255,size=(len(classes),3))

net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")

video="koridor_video2.mp4"
cap=cv2.VideoCapture(video)

if cap.isOpened()== False :
    print("hata")
while True:
    #videoyu nasıl okuyacağız:
    ret , frame= cap.read()
    #ret basarılı olup olmadıgı , frame okudugu resim
    if ret== True:
        time.sleep(0.005)# bunu yapmazsak çok hızlı akar
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize( frame, (300, 300)) , 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()
        for j in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, j, 2]
            if confidence > 0.5:
                idx = detections[0, 0, j, 1]
                idx = int(idx)
                box = detections[0, 0, j, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                label = "{}: {}".format(classes[idx], confidence)

                cv2.rectangle(frame, (startX, startY), (endX, endY), colors[idx], 1)
                y = startY - 16 if startY - 16 > 15 else startY + 16
                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors[idx], 1)

        cv2.imshow("video:",frame)
    else:
        break
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release() # videoyu serbest bırakıyoruz,videoyu almayı bırakıyoruz
cv2.destroyAllWindows()

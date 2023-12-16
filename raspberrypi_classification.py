import cv2
import time
import serial
from cvzone.ClassificationModule import Classifier

# 串列通訊設定
arduino_port = '/dev/ttyUSB0'
baud_rate = 9600
arduino = serial.Serial(arduino_port, baud_rate)
isArmMoving = False# 標誌變量
# 初始化相機視訊捕獲
cap = cv2.VideoCapture(0)

# 影像辨識模型和標籤  0 Metal  1 PG  2 paper  3 BG
cr = Classifier('keras_model.h5', 'label.txt')

# 定義裁切區域的座標
x, y, w, h ,t= 175, 20, 290, 440, 99 

while True:
    if arduino.in_waiting:
        armStatus = arduino.readline().decode().strip()
        isArmMoving = (armStatus == 'MOVING')
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
    
    # 裁切特定區域
    cropped_frame = frame[y:y + h, x:x + w]
    
    # 使用分類器對裁切後的區域進行分類
    pd = cr.getPrediction(cropped_frame)
    
    V = int(pd[1])#分類結果
    print(V) 
    if not isArmMoving:
        arduino.write(str(V).encode())
    
    
    # 在原始畫面上繪製矩形框，以顯示裁切區域
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
# 關閉通訊埠
arduino.close()

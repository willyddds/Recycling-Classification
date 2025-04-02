import cv2
import time
import serial
import numpy as np
import tensorflow as tf

# 串列通訊設定
arduino_port = '/dev/ttyUSB0'
baud_rate = 9600
arduino = serial.Serial(arduino_port, baud_rate)
isArmMoving = False  # 標誌變量

# 初始化相機
cap = cv2.VideoCapture(0)

# 載入 TFLite 模型
interpreter = tf.lite.Interpreter(model_path="0.35_quant.tflite")
interpreter.allocate_tensors()

# 取得輸入與輸出細節
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# 定義裁切區域的座標
x, y, w, h = 180, 0, 250, 200

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))

    # 裁切特定區域
    cropped_frame = frame[y:y + h, x:x + w]
    # 轉換成模型輸入格式
    input_shape = input_details[0]['shape']
    input_data = cv2.resize(cropped_frame, (input_shape[1], input_shape[2]))
    input_data = np.expand_dims(input_data.astype(np.float32) / 255.0, axis=0)

    # 進行推論
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # 取得分類結果
    V = int(np.argmax(output_data))
    confidence = float(np.max(output_data))

    # 接收手臂狀態
    if arduino.in_waiting:
        armStatus = arduino.readline().decode().strip()
        isArmMoving = (armStatus == "MOVING")

    # 傳送分類結果給手臂
    if not isArmMoving and V != 3:
        arduino.write(str(V).encode())
        print("Prediction:", V)
        isArmMoving = True

    # 畫框
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()

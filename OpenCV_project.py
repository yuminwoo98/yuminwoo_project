import cv2
import datetime
import time
from ultralytics import YOLO
import numpy as np
from twilio.rest import Client as TwilioClient

model = YOLO("C:/python/yoloTest/yolov8s.pt")


MSGsend = cv2.imread("msg.png", cv2.IMREAD_UNCHANGED)

alpha_channel = MSGsend[:, :, 3]
alpha_channel[:] = 0
MSGsend = cv2.cvtColor(MSGsend, cv2.COLOR_BGRA2BGR)

MSGsend = cv2.resize(MSGsend, (MSGsend.shape[1] // 4, MSGsend.shape[0] // 4))  # 내가 준비한 이미지를 웹캠 화면의 1/4 크기로 조정

classNames = [ "knife"]

myColor = (0, 0, 255)

capture_enabled = True
pre_capture_time = time.time()
captured_image = None  # 캡처된 이미지 저장 변수
display_webcam = True  # 웹캠 화면 표시 여부
SendMSG = True


def imgDetector(img):
    global capture_enabled, prev_capture_time, captured_image, display_webcam ,SendMSG

    current_time = time.time()

    # 이미지 크기 변경
    img = cv2.resize(img, dsize=None, fx=1.0, fy=1.0)

    # YOLO 객체 검출
    yolo_results = model(img, stream=True)
    
    for r in yolo_results:
        boxes = r.boxes
        for box in boxes:
            conf = box.conf[0]
            cls = int(box.cls[0])
            currentClass = classNames[cls]

            if currentClass == "knife":
                # "knife" 객체를 인식한 경우 해당 위치에 경계 상자 표시
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1
                cv2.rectangle(img, (x1, y1), (x2, y2), myColor, thickness=2)
                cv2.putText(
                    img,
                    f"{currentClass} {conf:.2f}",
                    (max(0, x1), max(35, y1)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    myColor,
                    thickness=2
                )

                if currentClass == "knife" and capture_enabled == True:
                    # "knife" 객체를 감지한 경우, MSGsend 이미지를 오른쪽 상단에 표시
                    img[0:MSGsend.shape[0], -MSGsend.shape[1]:] = MSGsend
                    
                    captured_image = img.copy()
                    
                    # 이미지를 파일로 저장
                    suffix = datetime.datetime.now().strftime('%y%m%d_%H%M%S')
                    fileName = suffix + '.png'
                    print("C:/python/object-Detection/" + fileName)
                    cv2.imwrite(fileName, captured_image)


                    #문자전송  테스트 할 때 아니면 비활성화 
                    if SendMSG == True:
                        account_sid = '~~~~'
                        auth_token = '~~~~'
                        twilio_client   = TwilioClient(account_sid, auth_token)

                        messege = twilio_client.messages.create(
                            to ="+82~~~~",
                            from_="+~~~~",
                            body="흉기 소지자 의심상황"
                        )
                        print(messege.sid)
                    
                    
                    # 캡처 후 일정 시간 동안 캡처 비활성화
                    SendMSG = False
                    capture_enabled = False
                    prev_capture_time = current_time
                    display_captured_image = True 

    if not capture_enabled and current_time - prev_capture_time >= 3.0:
        capture_enabled = True
        SendMSG = True

    return img

def main():
    camera = cv2.VideoCapture(cv2.CAP_DSHOW + 0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    while True:
        _, frame = camera.read()
        
        if display_webcam:
            retImg = imgDetector(frame)
        
        cv2.imshow("Webcam", retImg)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
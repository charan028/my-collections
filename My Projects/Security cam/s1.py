import cv2
import time
import datetime
# 0,1,2,3 indicates respective devices
cap = cv2.VideoCapture(0)

# for face detection and body detection cascade classifier
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_fullboy.xml")
detection = False
# 3,4==width,height
detectection_stopped_time = None
timer_started = False
seconds_to_detect = 5
frame_size = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
# fourcc=format,20=fps,frame_size=detect faces
# out = cv2.VideoWriter("video.mp4", fourcc, 20, frame_size)
while True:
    # neglected variable _
    _, frame = cap.read()
    # for classification we need to covert to grascale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # scale factor predicts accuracy images x-(1.1-1.5)  min no of neighbors (nof of boxes 3-6) y-()
    faces = face_cascade.detectMultiScale(gray, 1.2, 5)
    bodies = face_cascade.detectMultiScale(gray, 1.2, 5)
    if len(faces)+len(bodies) > 0:
        if detection:
            timer_started = False
        else:
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%y-%H-%M-%S")
            out = cv2.VideoWriter(
                f"{current_time}.mp4", fourcc, 20, frame_size)
            print("recording started")
    elif detection:
        if timer_started:
            if time.time()-detectection_stopped_time > seconds_to_detect:
                detection = False
                timer_started = False
                out.release()
                print("Stopped video Recording!")
        else:
            timer_started = True
            detectection_stopped_time = time.time()
    if detection:
        out.write(frame)
    # for rectangular frames
    # for (x, y, width, height) in faces:
    #     cv2.rectangle(frame, (x, y), (x+width, y+height), (255, 0, 0), 3)

    cv2.imshow("camera", frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

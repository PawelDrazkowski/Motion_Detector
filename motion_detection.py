import cv2 
from datetime import datetime
import pandas as pd 

video = cv2.VideoCapture(0)

first_frame = None
status_list = [None, None]
times = [] 
df = pd.DataFrame(columns = ["Start", "End"])

while True: 
    check, frame = video.read()

    status = 0 
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (21,21), 0) #blur image for better accuracy while calculating difference between images

    if first_frame is None:
        first_frame = gray_frame
        continue 

    delta_frame = cv2.absdiff(first_frame, gray_frame)
    tresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    tresh_frame = cv2.dilate(tresh_frame, None, iterations=5)

    (cnts, _) = cv2.findContours(tresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #generate contours of detected object

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status = 1 
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

    status_list.append(status)
    if status_list[-1] == 1 and status_list[-2] == 0: #detect apperance of an object 
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1: #detect disapperance of the object
        times.append(datetime.now())
        
    #cv2.imshow("Frame", gray_frame)  
    #cv2.imshow("Delta", delta_frame)    
    #cv2.imshow("Treshold frame", tresh_frame)
    cv2.imshow("Color frame", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        if status == 1: 
            times.append(datetime.now())
        break

print(status_list)
print(times)    

for i in range(0, len(times), 2):
    df = df.append({"Start":times[i], "End":times[i+1]}, ignore_index=True)

df.to_csv("Times.csv")
video.release()
cv2.destroyAllWindows()
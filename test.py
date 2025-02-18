from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime

from win32com.client import Dispatch

def speak(str1):
    speak = Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)

# Load trained model and data
with open('data/names.pkl', 'rb') as w:
    LABELS = pickle.load(w)
with open('data/usns.pkl', 'rb') as u:
    USNS = pickle.load(u)
with open('data/faces_data.pkl', 'rb') as f:
    FACES = pickle.load(f)

# Ensure consistency in data length
min_length = min(len(FACES), len(LABELS), len(USNS))
FACES = FACES[:min_length]
LABELS = LABELS[:min_length]
USNS = USNS[:min_length]

# Initialize KNN classifier
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
imgBackground = cv2.imread("present.jpg")

COL_NAMES = ['NAME', 'USN', 'TIME']

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3 ,5)
    
    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50,50)).flatten().reshape(1,-1)
        
        output = knn.predict(resized_img)
        idx = np.where(LABELS == output)[0][0]  # Find index of predicted label
        
        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 1)
        cv2.rectangle(frame, (x,y-40), (x+w, y), (50,50,255), -1)
        cv2.putText(frame, LABELS[idx], (x,y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        
        # Check for key press to mark attendance
        k = cv2.waitKey(1)
        if k == ord('o'):
            speak("Attendance Taken..")
            attendance = [LABELS[idx], USNS[idx], timestamp]
            
            # Check if attendance file exists for today's date
            attendance_file = f"Attendance/Attendance_{date}.csv"
            file_exists = os.path.isfile(attendance_file)
            
            # Write attendance to CSV
            with open(attendance_file, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow(COL_NAMES)
                writer.writerow(attendance)
            
            # Delay and reset
            time.sleep(5)
    
    imgBackground[162:162 + 480, 55:55 + 640] = frame
    cv2.imshow("Frame", imgBackground)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()

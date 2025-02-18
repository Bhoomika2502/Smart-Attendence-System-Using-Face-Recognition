import cv2
import pickle
import numpy as np
import os

# Initialize video capture and face cascade classifier
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

# Initialize empty lists and counters
faces_data = []
names = []
usns = []
i = 0

# Prompt user for name and USN
name = input("Enter Your Name: ")
usn = input("Enter Your USN: ")

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3 ,5)
    
    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50,50))
        
        if len(faces_data) <= 100 and i % 10 == 0:
            faces_data.append(resized_img)
            names.append(name)
            usns.append(usn)
        
        i += 1
        cv2.putText(frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 1)
    
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    
    if k == ord('q') or len(faces_data) == 100:
        break

video.release()
cv2.destroyAllWindows()

# Convert lists to numpy arrays
faces_data = np.asarray(faces_data)
faces_data = faces_data.reshape(100, -1)

# Save names and usns to pickle files
if 'names.pkl' not in os.listdir('data/'):
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(names, f)
else:
    with open('data/names.pkl', 'rb') as f:
        existing_names = pickle.load(f)
    names = existing_names + names
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(names, f)

if 'usns.pkl' not in os.listdir('data/'):
    with open('data/usns.pkl', 'wb') as f:
        pickle.dump(usns, f)
else:
    with open('data/usns.pkl', 'rb') as f:
        existing_usns = pickle.load(f)
    usns = existing_usns + usns
    with open('data/usns.pkl', 'wb') as f:
        pickle.dump(usns, f)

# Save faces data to pickle file
if 'faces_data.pkl' not in os.listdir('data/'):
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces_data, f)
else:
    with open('data/faces_data.pkl', 'rb') as f:
        existing_faces = pickle.load(f)
    faces = np.append(existing_faces, faces_data, axis=0)
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces, f)

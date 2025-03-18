import cv2
import streamlit as st
import numpy as np
import tempfile
from ultralytics import YOLO
import datetime
import time
import notify
import os
import time
cap = cv2.VideoCapture(0)

st.title("SDS-AI weapon detection systems")
frame_placeholder = st.empty()
mode = st.toggle("Activated SDS-AI")

prev_frame= 0
curr_frame = 0
fps = 0
last_notifi_time = 0
model = YOLO('best17.pt')
#model = YOLO("yolov8n.pt")

while cap.isOpened() and mode:
    ret, frame = cap.read()

    if not ret:
        st.write("The video capture has ended.")
        break

    #Display time
    curr_datetime = datetime.datetime.now()
    datetime_str = curr_datetime.strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(frame, datetime_str, (10,frame.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    
    #FPS
    curr_frame= time.time()  
    fps = 1 / (curr_frame - prev_frame)  
    prev_frame = curr_frame  
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 255), 1)
    
    if ret:
        results = model(frame)
        annotated_frame = results[0].plot()
        
        # Extract bounding boxes, classes, names, and confidences
        boxes = results[0].boxes.xyxy.tolist()
        classes = results[0].boxes.cls.tolist()
        names = results[0].names
        confidences = results[0].boxes.conf.tolist()

        # Iterate through the results
        for box, cls, conf in zip(boxes, classes, confidences):
            if conf>=0.75 :
                curr_time = time.time()
                if curr_time - last_notifi_time >= 30 :
                    timestamp = curr_datetime.strftime("%Y%m%d%H%M%S")
                    filename = f"weapon_detected_{timestamp}.jpg"
                    #cv2.imwrite(os.path.join(path,filename ),annotated_frame)
                    cv2.imwrite(filename, annotated_frame)
                    notify.send_line_notify(filename, confidences)
                    cv2.imshow("frame",annotated_frame)
                    #arduipy.arduipy(5,"ON")
                    last_notifi_time = curr_time
                
                
        # Convert the frame from BGR to RGB format
        #annotated_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Display the frame using Streamlit's st.image
        frame_placeholder.image(annotated_frame, channels="BGR")

   # Break the loop if the 'q' key is pressed or the user clicks the "Stop" button
    if cv2.waitKey(1) & 0xFF == ord("q") or not mode: 
        break

cap.release()
cv2.destroyAllWindows()
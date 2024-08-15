# import streamlit as st
# from streamlit_webrtc import webrtc_streamer
# import av
# import cv2

# def video_frame_callback(frame):
#     img = frame.to_ndarray(format="bgr24")

#     # Here you can process the image frame with OpenCV
#     # For example, converting to grayscale
#     img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     img_gray = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

#     return av.VideoFrame.from_ndarray(img_gray, format="bgr24")

# st.title("Webcam Stream with Streamlit")

# webrtc_streamer(key="example", video_frame_callback=video_frame_callback)

# import streamlit as st
# from streamlit_webrtc import webrtc_streamer
# import av
# import cv2
# import face_recognition

# def video_frame_callback(frame):
#     img = frame.to_ndarray(format="bgr24")

#     # Detect faces in the frame
#     face_locations = face_recognition.face_locations(img)

#     # Draw bounding boxes around the faces
#     for (top, right, bottom, left) in face_locations:
#         cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)

#     return av.VideoFrame.from_ndarray(img, format="bgr24")

# st.title("Webcam Stream with Face Recognition")

# webrtc_streamer(key="example", video_frame_callback=video_frame_callback)

import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import cv2
import face_recognition

# Global variable to keep track of frame processing
process_this_frame = True

def video_frame_callback(frame):
    global process_this_frame
    img = frame.to_ndarray(format="bgr24")

    # Reduce frame size for faster processing
    small_img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    rgb_small_img = small_img[:, :, ::-1]

    if process_this_frame:
        # Detect faces in the smaller frame
        face_locations = face_recognition.face_locations(rgb_small_img)
        process_this_frame = False
    else:
        face_locations = []
        process_this_frame = True

    # Scale back up face locations since we detected on a smaller frame
    face_locations = [(top*4, right*4, bottom*4, left*4) for (top, right, bottom, left) in face_locations]

    # Draw bounding boxes around the faces
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)

    return av.VideoFrame.from_ndarray(img, format="bgr24")

st.title("Webcam Stream with Face Recognition")

webrtc_streamer(key="example", video_frame_callback=video_frame_callback)


import cv2
import streamlit as st
import s3.s3 as s3
import face_recogntion.face_recogntion as face_recogntion
import os
import sql.user_infor as database
from streamlit_webrtc import (
    WebRtcMode,
    webrtc_streamer,
    ClientSettings
)
import queue
import av

# class VideoProcessor(VideoProcessorBase):
#     def __init__(self):
#         self.image_count = 0

#     def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
#         # Process the video frame here if needed

#         # Increment image count
#         self.image_count += 1

#         # Check if 10 images have been captured
#         if self.image_count >= 100:
#             # Stop the video stream
#             self.webrtc_ctx.video_processor.stop()

#         return frame

# def main():
    
# st.title("Webcam Live Feed")
def face_record(name, email, userID):
    WEBRTC_CLIENT_SETTINGS = ClientSettings(
    rtc_configuration={
        "iceServers": [{
            "urls": ["stun:stun.l.google.com:19302"]
        }]
    },
    media_stream_constraints={
        "video": True,
        "audio": False
    },
)
    webrtc_ctx = webrtc_streamer(
        key="loopback",
        mode=WebRtcMode.SENDONLY,
        client_settings=WEBRTC_CLIENT_SETTINGS,
    )
    folder_path = f"./{userID}"
    os.makedirs(folder_path, exist_ok=True)
    image_loc = st.empty()
    count  = 0
    while True:
        try:
            if webrtc_ctx.video_receiver:
                frame = webrtc_ctx.video_receiver.get_frame(timeout=1)
                count += 1
                img_rgb = frame.to_ndarray(format="rgb24")
                image_loc.image(img_rgb)
                cv2.imwrite(f'{folder_path}/{userID}_{count}.jpg', img_rgb)
                if count > 10:
                    print("aaaaaaaaaaaaaaa")
                    webrtc_ctx.video_receiver.stop()
                    image_loc.image([])
                    break
        except queue.Empty:
                print("Queue is empty. Stop the loop.")
                webrtc_ctx.video_receiver.stop()
                break

        

        
    # Create folder based on email
    
    # Upload images to S3
    s3.upload_images(userID)
    photos = s3.get_images_name_in_folder(userID)
    # print(photos)
    list_faces = face_recogntion.add_faces_to_collection(photos)
    face_recogntion.create_user(userID)
    face_recogntion.associate_faces(userID, list_faces)
    # Delete the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        os.remove(file_path)
    os.rmdir(folder_path)
    database.insert(userID=userID, name=name, email=email)
    st.success(f"Okkiiiii {name}, {userID}")
    

def main():
    st.title("Add User")
    name = st.text_input("Enter your name:")
    email = st.text_input("Enter your email:")
    userid = st.text_input("Enter your userID:")
    if name and email and userid:
        if database.search_user(userid) is None:
            face_record(name, email, userid)
        else :
            st.warning("User is exits")
            


    
if __name__ == "__main__":
    main()
import cv2
import streamlit as st
import s3.s3 as s3
import face_recogntion.face_recogntion as face_recogntion
import send_mail.send_mail as send_mail
import os
import numpy as np
from PIL import Image
import time
import sql.user_infor as user_infor
# st.title("Webcam Live Feed")

def main():
    st.title("Check In")
    picture = st.camera_input("Take a picture")

    if picture:
        image_name = f"check_in_image_{time.time() * 1000}.jpg"
        img = Image.open(picture)
        img.save(f"{image_name}")
        # To convert PIL Image to numpy array:
        # img_bytes = img.tobytes()
        reponse = face_recogntion.search_users_by_image(image_name)
        print("aaaaaaaaaaaaaaaaaaaa", reponse)
        if len(reponse) > 0:
            userID = reponse[0]["User"]["UserId"]
            if userID is not None:
                url = s3.upload_image_get_url(image_name, userID)
                print("userrrrrrrr", userID)
                email = user_infor.search_user(userID)[2]
                print(email, url)
                send_mail.send_verify_checkin(email=email, url=url)
                st.success("Check in Success")
        else:
            st.warning("Check in Fail")
        os.remove(image_name)
    
if __name__ == "__main__":
    main()
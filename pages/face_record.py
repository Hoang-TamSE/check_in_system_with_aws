import cv2
import streamlit as st
import s3.s3 as s3
import face_recogntion.face_recogntion as face_recogntion
import os
import sql.user_infor as database
# st.title("Webcam Live Feed")
def face_record(name, email, userID):
    # Create folder based on email
    folder_path = f"./{userID}"
    os.makedirs(folder_path, exist_ok=True)

    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)
    count = 0  # Declare count as a global variable
    while True:
        count += 1
        _, frame = camera.read()
        frame_cvt = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame_cvt)
        
        # image_path = os.path.join(folder_path, f"{userID}_{count}.jpg")
        cv2.imwrite(f'{folder_path}/{userID}_{count}.jpg', frame)
        
        if count >= 10:
            print("aaaaaaaaaaaaaaaaaa")
            break
    
    st.write('Stopped')
    camera.release()
    FRAME_WINDOW.image([])
    
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
    
    st.success(f"Okkiiiii {name}, {userID}")

def main():
    st.title("Add User")
    name = st.text_input("Enter your name:")
    email = st.text_input("Enter your email:")
    userid = st.text_input("Enter your userID:")
    if name and email and userid:
        if database.search_user(userid) is None:
            if st.button("Go to record Face"):
                database.insert(userID=userid, name=name, email=email)
                face_record(name, email, userid)
        else :
            st.warning("User is exits")
            


    
if __name__ == "__main__":
    main()
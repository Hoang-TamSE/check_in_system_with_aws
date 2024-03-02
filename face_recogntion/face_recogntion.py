# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
from botocore.exceptions import ClientError
import logging
logger = logging.getLogger(__name__)
bucket = 'facebucket1608'
collection_id = 'face-recognition-workshop'
profile_name = 'default'
session = boto3.Session(profile_name=profile_name)
client = session.client('rekognition')

def search_face(photo):
    threshold = 70
    maxFaces=1
    response=client.search_faces_by_image(CollectionId=collection_id,
                                Image={'S3Object':{'Bucket':bucket,'Name':photo}},
                                FaceMatchThreshold=threshold,
                                MaxFaces=maxFaces)

                                
    faceMatches=response['FaceMatches']
    print ('Matching faces')
    for match in faceMatches:
            print ('FaceId:' + match['Face']['FaceId'])
            print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
            print
def create_collection():

    # Create a collection
    print('Creating collection:' + collection_id)
    response = client.create_collection(CollectionId=collection_id)
    print('Collection ARN: ' + response['CollectionArn'])
    print('Status code: ' + str(response['StatusCode']))
    print('Done...')

def add_faces_to_collection(photos):
    list_faceid = []
    for photo in photos:
        response = client.index_faces(CollectionId=collection_id,
                                    Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
                                    ExternalImageId=photo.split("/")[-1],
                                    MaxFaces=1,
                                    QualityFilter="AUTO",
                                    DetectionAttributes=['ALL'])
        for faceRecord in response['FaceRecords']:
            list_faceid.append(faceRecord['Face']['FaceId'])

    return list_faceid
def associate_faces(user_id, face_ids):
    """
    Associate stored faces within collection to the given user

    :param collection_id: The ID of the collection where user and faces are stored.
    :param user_id: The ID of the user that we want to associate faces to
    :param face_ids: The list of face IDs to be associated to the given user

    :return: response of AssociateFaces API
    """
    print(f'Associating faces to user: {user_id}, {face_ids}')
    logger.info(f'Associating faces to user: {user_id}, {face_ids}')
    try:
        response = client.associate_faces(
            CollectionId=collection_id,
            UserId=user_id,
            FaceIds=face_ids
        )
        print(f'- associated {len(response["AssociatedFaces"])} faces')
    except ClientError:
        logger.exception("Failed to associate faces to the given user")
        raise
    else:
        print(response)
        return response
def create_user(user_id):
    """
    Creates a new User within a collection specified by CollectionId. 
    Takes UserId as a parameter, which is a user provided ID which 
    should be unique within the collection.

    :param collection_id: The ID of the collection where the indexed faces will be stored at.
    :param user_id: ID for the UserID to be created. This ID needs to be unique within the collection.
    
    :return: The indexFaces response
    """
    try:
        logger.info(f'Creating user: {collection_id}, {user_id}')
        client.create_user(
            CollectionId=collection_id,
            UserId=user_id
        )
        print("Create user success")
    except ClientError:
        logger.exception(f'Failed to create user with given user id: {user_id}')
        raise

def load_image(file_name):
    """
    helper function to load the image for indexFaces call from local disk

    :param image_file_name: The image file location that will be used by indexFaces call.
    :return: The Image in bytes
    """
    print(f'- loading image: {file_name}')
    with open(file_name, 'rb') as file:
        return {'Bytes': file.read()}
    
def search_users_by_image(image_file):
    """
    SearchUsersByImage operation with user ID provided as the search source

    :param collection_id: The ID of the collection where user and faces are stored.
    :param image_file: The image that contains the reference face to search for.

    :return: response of SearchUsersByImage API
    """
    logger.info(f'Searching for users using an image: {image_file}')
    try:
        response = client.search_users_by_image(
            CollectionId=collection_id,
            Image=load_image(image_file),
            MaxUsers=1,
            UserMatchThreshold=70
        )
        print(f'- found {len(response["UserMatches"])} matches')
        print([f'- {x["User"]["UserId"]} - {x["Similarity"]}%' for x in response["UserMatches"]])
        return response["UserMatches"]
    except ClientError:
        logger.exception(f'Failed to perform SearchUsersByImage with given image: {image_file}')
        raise


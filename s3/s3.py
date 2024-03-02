import boto3
from botocore.exceptions import ClientError
import logging
import glob

logger = logging.getLogger(__name__)
bucket = 'facebucket1608'
client = boto3.client('s3')

def upload_images(folder_name):
    photos = glob.glob(f"./{folder_name}/*.jpg")
    print(photos)
    for photo in photos:
        print(photo)
        split_path = photo.split("\\")
        client.upload_file(photo, bucket, f'{folder_name}/{split_path[-1]}')

def get_images_name_in_folder(folder_name):
    photos = []
    response = client.list_objects_v2(
        Bucket=bucket,
        Prefix=f'{folder_name}/')
    print(response)
    for content in response.get('Contents', []):
        photos.append(content['Key'])
    return photos

def upload_image_get_url(photo, folder_name):
    client.upload_file(photo, bucket, f'{folder_name}/{photo.split("/")[-1]}')
    response = client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket,
                                                            'Key': f'{folder_name}/{photo.split("/")[-1]}'},
                                                    ExpiresIn=60*60*12)
    return response

print(get_images_name_in_folder("abcc"))





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

def create_collection():
    # Create a collection
    print('Creating collection:' + collection_id)
    response = client.create_collection(CollectionId=collection_id)
    print('Collection ARN: ' + response['CollectionArn'])
    print('Status code: ' + str(response['StatusCode']))
    print('Done...')
create_collection()
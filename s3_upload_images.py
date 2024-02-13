import os
import yaml
import boto3
from botocore.exceptions import ClientError
import upload

def load_config():
    """
    Function to get configuration
    return: config: configurations from yaml file
    """
    with open('config.yml', 'r') as config_file:
      config = yaml.load(config_file)
      return config

def initiate_session(config, client):
    """
    Function to initiate session in s3
    param: config: configuration to add access key and id 
    param: client: s3 in aws
    return: client: when it is called session is initiated for client
    """
    session = boto3.Session(
        aws_access_key_id=config['aws_access_key_id'],
        aws_secret_access_key=config['aws_secret_access_key'],
        region_name='india'
    ) 
    print(session)
    client = session.resource(client)
    return client

def upload_file(client, fileobj, bucket, key):
    """
    Function to upload list of all images from directories and subdirectories in a given path
    param:client: aws s3 session details
    param: fileobj: file to be uploaded
    param: bucket: bucket upload
    param: key: image name for testing
    return: success when it is called uploaded else error will be displayed
    """
    with open(fileobj, 'rb') as data:
        try:
            client.Bucket(bucket).put_object(
                Body = data,
                Bucket = bucket,
                Key = key,
                ContentType = 'image/jpeg'
            ) 
            print('success')
            return 'success'

        except ClientError as e:
          print('error: %s') % e
          return 'error'

def main():
    """
    Function to upload images to aws s3
    return: status: status of s3 instance
    """
    config = load_config()
    client = initiate_session(config, 's3')
    filelist = [(os.path.join(root,file)) for root, dirs, files in os.walk(config[PATH]) for file in files]
    images = [file for file in filelist if file.endswith(config[IMAGE_EXTENSIONS])]
    docs = [file for file in filelist if not file.endswith(config[IMAGE_EXTENSIONS])]
    for file in images:
      fileobj = file
      bucket = config['upload_bucket']
      key = 'testimg.jpg'
      status = upload_file(client, fileobj, bucket, key)
    return status 

if __name__ == '__main__':
    main()

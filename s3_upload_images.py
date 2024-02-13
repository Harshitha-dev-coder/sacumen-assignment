import os
import yaml
import boto3
from botocore.exceptions import ClientError
import upload

def load_config():
    with open('config.yml', 'r') as config_file:
      config = yaml.load(config_file)
      return config

def initiate_session(config, client):
    session = boto3.Session(
        aws_access_key_id=config['aws_access_key_id'],
        aws_secret_access_key=config['aws_secret_access_key'],
        region_name='india'
    ) 
    print(session)
    client = session.resource(client)
    return client

def upload_file(client, fileobj, bucket, key):
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

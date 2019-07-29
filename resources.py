import boto3
from config import S3_BUCKET, S3_KEY, S3_SECRET
from flask import session

def _get_s3_resource():
    if S3_KEY and S3_SECRET:
        return boto3.resource(
            's3',
            aws_access_key_id=S3_KEY,
            aws_secret_access_key=S3_SECRET
        )
    else:
        return boto3.resource('s3')


def get_bucket():
    s3_resource = _get_s3_resource()
    if 'bucket' in session:
        bucket = session['bucket']
    else:
        bucket = S3_BUCKET

    return s3_resource.Bucket(bucket)


def get_buckets_list():
    client = boto3.client('s3')
    return client.list_buckets().get('Buckets')

def get_all_objects_from_bucket():
    client = boto3.client('s3')
    bucket = get_bucket()
    all_objects = client.list_objects_v2(Bucket=bucket.name)

    file_names = [file.get("Key") for file in all_objects.get("Contents", [])]
    return file_names

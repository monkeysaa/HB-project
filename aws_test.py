import boto3
import os 

# Let's use Amazon S3
s3 = boto3.resource('s3')
# AWS can access environmental variables with particular names. Already doing this. 
client = boto3.client('s3')

for bucket in s3.buckets.all():
    print(bucket.name)

# s3.download_file('BUCKET_NAME', 'OBJECT_NAME', 'FILE_NAME')
# client.download_file('hackbright-project', 'Jonah\'s Frog.png', 'test.png')

client.upload_file('server.py', 'hackbright-project', 'server.py')
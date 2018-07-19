#!/usr/bin/python
import boto3
import gzip
import json
import sys

ec2 = boto3.client('ec2')
s3 = boto3.resource('s3')
sns = boto3.client('sns')

def send_to_sns_topic(message):
        response = sns.publish(
                TopicArn='arn:aws:sns:eu-west-1:380222987620:LambdaNotifications',
                Message=message,
                Subject='CloudTrail Event'
                )

def analyse_cloudtrail_output(event):
        for record in event['Records']:
                s3_bucket = record['s3']['bucket']['name']
                s3_path = record['s3']['object']['key']
                s3_size = record['s3']['object']['size']

                if s3_size <= 524288000:
#                       print("CloudTrail filename %s bytes is less than available 500MB lambda scratch space" % (s3_size))
                        # Get the absolute CloudTrail filename to download
                        s3_filename = s3_path.split("/",7)[-1]
                        # Download file to scratch space (limited to 500MB)
                        s3.meta.client.download_file(s3_bucket, s3_path, '/tmp/%s' % (s3_filename))
                        # Decompress and read cloudtrail events
                        handler = gzip.open('/tmp/%s' % (s3_filename), 'rb')
                        content = handler.read()
                        howbig = sys.getsizeof(content) # Get size of data chunk
#                        print("Decompressed CloudTrail data is %d bytes" % (howbig))

                        # Convert back to JSON and Loop through the CloudTrail events
                        cloudtraillog = json.loads(content)
                        for records in cloudtraillog['Records']:
#                                print("Test Data: %s" % (records['eventName']))
                                if records['eventName'] == "RunInstances":
#                                        print("A user has executed RunInstances")
                                        username = records['userIdentity']['sessionContext']['sessionIssuer']['userName']
                                        region = records['awsRegion']
                                        datetimevar = records['userIdentity']['sessionContext']['attributes']['creationDate']
                                        instanceId = records['responseElements']['instancesSet']['items'][0]['instanceId']
                                        message = "WARNING: A new un-tagged EC2 instance has been created, UserName: %s / Region: %s / DateTime: %s / insanceID: %s" % (username,region,datetimevar,instanceId)
                                        send_to_sns_topic(message)
                        handler.close()
                else:
                        print("CloudTrail file is too large, skipping %s" % (s3_filename))

def lambda_handler(event, context):
        analyse_cloudtrail_output(event)
        return {
        }

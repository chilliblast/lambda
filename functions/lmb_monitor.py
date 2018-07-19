#!/usr/bin/python
import boto3
import json
import time

start_time = time.strftime("%d%m%Y")

client = boto3.client('cloudtrail')

context = ""; event = ""

#def send_to_sns_topic(message):
#        response = sns.publish(
#                TopicArn='arn:aws:sns:eu-west-1:380222987620:LambdaNotifications',
#                Message=message,
#                Subject='CloudTrail Event'
#                )

def analyse_cloudtrail_output(event):
	response = client.lookup_events(
		LookupAttributes=[
			{
				'AttributeKey':	'EventName',
				'AttributeValue': 'StartInstances'
			},
		],
	)
	relen = len(response)
	for x in response['Events']:
		bin = x['CloudTrailEvent']
		print("CloudTrailEvent data contains: %s" % (bin))
		jsonbin = json.loads(bin)
		instance_raw = jsonbin['responseElements']['instancesSet']['items']
		for x in instance_raw:
			print("x is now: %s" % (x))
		username = jsonbin['userIdentity']['userName']
		creationdate = jsonbin['userIdentity']['sessionContext']['attributes']['creationDate']
		eventTime = jsonbin['eventTime']
		sourceIPaddress = jsonbin['sourceIPAddress']
		instanceId = jsonbin['requestParameters']['instancesSet']['items'][0]
		print("username %s with the client IP of %s, started an ec2 instance (%s) at %s" % (username,sourceIPaddress,instanceId,eventTime))

def lambda_handler(event, context):
        analyse_cloudtrail_output(event)
        return {
        }

lambda_handler(event, context)

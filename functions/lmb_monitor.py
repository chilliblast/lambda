#!/usr/bin/python
import boto3
import json
import time

start_time = time.strftime("%d%m%Y")

client = boto3.client('cloudtrail')

context = ""; event = ""; instanceid = []

#def send_to_sns_topic(message):
#        response = sns.publish(
#                TopicArn='arn:aws:sns:eu-west-1:380222987620:LambdaNotifications',
#                Message=message,
#                Subject='CloudTrail Event'
#                )

def analyse_cloudtrail_output(instanceid,event):
	response = client.lookup_events(
		LookupAttributes=[
			{
				'AttributeKey':	'EventName',
				'AttributeValue': 'RunInstances'
			},
		],
		MaxResults=1000,
	)
	
	for x in response['Events']:
		bin = x['CloudTrailEvent']
		jsonbin = json.loads(bin)
		print("\n")
		print("*** NEW ENTRY ***")
		print("\n")
		print("jsonbin contains: %s" % (jsonbin))
		print("\n")
		if jsonbin['responseElements']:
                        print("\n")
                        print("responseElements is NOT null")
                        print("\n")
                        instance_raw = jsonbin['responseElements']['instancesSet']['items']
                        type = jsonbin['userIdentity']['type']
                        if 'invokedBy' in jsonbin['userIdentity']:
#                                username = jsonbin['userIdentity']['userName']
				username = jsonbin['sessionContext']['userName']
                        else:
                                username = "not found"
		else:
                        print("responseElements is null")
                        print("\n")
			
		creationdate = jsonbin['userIdentity']['sessionContext']['attributes']['creationDate']
		eventTime = jsonbin['eventTime']
		agent = jsonbin['userAgent']
		sourceIPaddress = jsonbin['sourceIPAddress']
		for x in instance_raw:
			instanceid.append(str(x['instanceId']))
			inst = ','.join(instanceid)
	
		print("username %s (%s via %s) with a client IP of %s, started an ec2 instance (%s) at %s" % (username,type,agent,sourceIPaddress,inst,eventTime))
		instanceid=[]; inst=""; username=""

def lambda_handler(event, context):
        analyse_cloudtrail_output(instanceid,event)
        return {
        }

lambda_handler(event, context)

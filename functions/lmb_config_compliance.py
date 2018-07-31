#!/usr/bin/python
import boto3
import json
import time

start_time = time.strftime("%d%m%Y")

#def send_to_sns_topic(message):
#        response = sns.publish(
#                TopicArn='arn:aws:sns:eu-west-1:380222987620:LambdaNotifications',
#                Message=message,
#                Subject='CloudTrail Event'
#                )

def analyse_config_output(event,context):
	print("Raw event variable contains: %s" % (event))
	print("\n")
	print("Raw context variable contains: %s" % (context))
	print("\n")
	for record in event['Records']:
		print("record variable is: %s" % (record))

def lambda_handler(event,context):
        analyse_config_output(event,context)
        return {
        }

lambda_handler(event,context)

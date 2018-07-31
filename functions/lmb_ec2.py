#!/usr/bin/python
import boto3
import json
import time

start_time = time.strftime("%d%m%Y")

ec2 = boto3.client('ec2')

context = ""; event = ""; instanceid = []

#def send_to_sns_topic(message):
#        response = sns.publish(
#                TopicArn='arn:aws:sns:eu-west-1:380222987620:LambdaNotifications',
#                Message=message,
#                Subject='CloudTrail Event'
#                )
def analyse_ec2_instances(instanceid,event):
        instance = ec2.describe_instances(
                Filters=[
                {
                        'Name' : 'launch-time',
                        'Values' : [
                                '2018, 7, 24, 7, 55, 23',
#			'Name': 'tag:Application',
#			'Values': [
#				'DEV',
                      ]
                }
                ]
        )

        for reservations in (instance["Reservations"]):
                for instance in (reservations["Instances"]):
                        instance_id = instance['InstanceId'];instance_name = instance['PrivateDnsName']
			print("instance_id is: %s" % (instance_id))
			print("\n")
			print("instance variable is set to: %s" % (instance))



def lambda_handler(event, context):
        analyse_ec2_instances(instanceid,event)
        return {
        }

lambda_handler(event, context)

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
			 'Name': 'instance-id',
			 'Values' : [
				'i-06fb4785bac7c09e6',
			 ]
#                        'Name' : 'launch-time',
#                        'Values' : [
#                                '2018, 7, 24, 7, 55, 23',
#			'Name': 'tag:Application',
#			'Values': [
#				'DEV',
		}
                      ]
        )
        running_state = instance['Reservations'][0]['Instances'][0]['State']['Name']
	instance_name = instance['Reservations'][0]['Instances'][0]['PrivateDnsName']
	instance_type = instance['Reservations'][0]['Instances'][0]['InstanceType']
	ssh_key = instance['Reservations'][0]['Instances'][0]['KeyName']
	print(running_state)
	print("instance_id is: %s // SSH key used is %s // instance type is: %s // instance name is: %s // instance state is: %s" % (instanceid,ssh_key,instance_type,instance_name,running_state))
	#print("\n")
	#print("instance variable is set to: %s" % (instance))



def lambda_handler(event, context):
        analyse_ec2_instances(instanceid,event)
        return {
        }

lambda_handler(event, context)

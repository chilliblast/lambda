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
	print("instance variable is set to: %s" % (list(instance['Reservations'][0]['Instances'])))

        for reservations in (instance["Reservations"]):
                for instance in (reservations["Instances"]):
                        instance_id = instance['InstanceId'];instance_name = instance['PrivateDnsName']
			ssh_key = instance['KeyName'];instance_type = instance['InstanceType']
			print("instance_id is: %s // SSH key used is %s // instance type is: %s" % (instance_id,ssh_key,instance_type))



def lambda_handler(event, context):
        analyse_ec2_instances(instanceid,event)
        return {
        }

lambda_handler(event, context)

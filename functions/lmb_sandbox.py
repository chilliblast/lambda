#!/usr/bin/python
import boto3
import json
import os
import time

start_time = time.strftime("%d%m%Y")

def get_instance_details(ResourceId):
        ec2 = boto3.client('ec2')
        instance = ec2.describe_instances(
                Filters=[
                {
                         'Name': 'instance-id',
                         'Values' : [
                                ResourceId,
                         ]
                }
                ]
        )
        instance_name = instance['Reservations']['Instances']['PrivateDnsName']
        ssh_key = instance['Reservations']['Instances']['KeyName'];instance_type = instance['Reservations']['Instances']['InstanceType']
        return(instance_name,instance_type,ssh_key)

def send_to_sns_topic(message):
        sns = boto3.client('sns')
        response = sns.publish(
                TopicArn = os.environ['TOPIC_ARN'],
                Message=message,
                Subject='AWS Tagging Compliance'
                )

def analyse_config_output(event):
#        print("Full event variable output: %s" %(event))
        ResourceType = event['detail']['newEvaluationResult']['evaluationResultIdentifier']['evaluationResultQualifier']['resourceType']
        ResourceId = event['detail']['resourceId']
        if 'oldEvaluationResult' in event['detail'] and 'newEvaluationResult' in event['detail']:
                OldComplianceType = event['detail']['oldEvaluationResult']['complianceType']
                NewComplianceType = event['detail']['newEvaluationResult']['complianceType']
                if NewComplianceType == 'COMPLIANT' and OldComplianceType == 'NON_COMPLIANT':
                        print("Previously NON_COMPLIANT Resource %s with Resource ID %s is now COMPLIANT" % (ResourceType,ResourceId))
                        message = "Previously NON_COMPLIANT Resource %s with Resource ID %s is now COMPLIANT" % (ResourceType,ResourceId)
                elif NewComplianceType == 'NON_COMPLIANT' and OldComplianceType == 'COMPLIANT':
                        print("Previously COMPLIANT Resource %s with Resource ID %s is now NON_COMPLIANT" % (ResourceType,ResourceId))
                        message = "Previously COMPLIANT Resource %s with Resource ID %s is now NON_COMPLIANT" % (ResourceType,ResourceId)
                elif NewComplianceType == 'NOT_APPLICABLE':
                        print("Previously NON_COMPLIANT Resource %s with Resource ID %s is no longer applicable (removed, terminated or no change)" % (ResourceType,ResourceId))
                        message = "Previously NON_COMPLIANT Resource %s with Resource ID %s is no longer applicable (removed, terminated or no change)" % (ResourceType,ResourceId)
        else:
                NewComplianceType = event['detail']['newEvaluationResult']['complianceType']
                print("Resource %s with Resource ID %s is %s" % (ResourceType,ResourceId,NewComplianceType))
                message = "Resource %s with Resource ID %s is %s" % (ResourceType,ResourceId,NewComplianceType)
        
        if ResourceType == 'AWS::EC2::Instance':
                get_instance_details(ResourceId)
                message = message + " " + instance_name + " " + instance_type + " " + ssh_key
        send_to_sns_topic(message)

def lambda_handler(event, context):
        analyse_config_output(event)
        return {
        }

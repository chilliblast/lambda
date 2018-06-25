#
# Custom Lambda function to query tags based on passed EC2 instance-id
# 
# Testing: Use EC2InstanceTest to test this function
#
# 16.02.2018 22:51 - added memoization (LRU)
import boto3
from functools import lru_cache
from joblib import Memory

@lru_cache(maxsize=16)
def pull_ec2_details(inst_id):
        global cachehit,instance_name,instance_id,LogAnalysis
        ec2 = boto3.client('ec2')
        instance = ec2.describe_instances(
			Filters=[
				{
					'Name' : 'tag-key',
					'Values': [
						'dswrx:group',
						  ]
				},
			],
            InstanceIds=[
                inst_id,
                ],
				DryRun=False
        )
        print("Raw instance var data is: ",instance)
        instance_name = instance['Reservations'][0]['Instances'][0]['PrivateDnsName']
        instance_id = instance['Reservations'][0]['Instances'][0]['InstanceId']
        LogAnalysis = instance['Reservations'][0]['Instances'][0]['Tags']
        cachehit = pull_ec2_details.cache_info()
        

def lambda_handler(event, context):
        print(event)
        inst_id = event['key1']
        print(inst_id)
#        pull_ec2_details.cache_clear()
        pull_ec2_details(inst_id)
        return {
            'Received Instance ID' : inst_id,
            'Actual Instance Name' : instance_name,
            'Actual Instance ID' : instance_id,
            'Actual LogAnalysis Tag set' : LogAnalysis,
            'Cache status is: ' : cachehit
        }

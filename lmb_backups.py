import boto3
import time

ec2 = boto3.client('ec2')

def execute_ec2_snapshot(instance_id,instance_name):
	global snapshot
	volumes = ec2.describe_instance_attribute(InstanceId=instance_id,Attribute='blockDeviceMapping')
	volen = len(volumes['BlockDeviceMappings'])
	for v_id in volumes['BlockDeviceMappings']:
		volume_id = v_id['Ebs']['VolumeId']
		start_time = time.strftime("%d%m%Y")
		snapshot = ec2.create_snapshot(
			Description=instance_name,
			VolumeId=volume_id,
			DryRun=False
		)
#		print("Snapshot %s taken of volume %s" % (snapshot['SnapshotId'], volume_id))
	
        	ec2.create_tags(
	        	DryRun=False,
   		    	Resources=[
		        	snapshot['SnapshotId'],
	        	],
    	    	Tags=[
        			{'Key': 'Name', 'Value': instance_id},
        			{'Key': 'Description', 'Value': 'Created by Lambda'},
        			{'Key': 'VolumeId', 'Value': volume_id},
				{'Key': 'Date', 'Value': start_time}
        		]
        	)

def pull_ec2_details():
	global instance_id,instance_name
	instance = ec2.describe_instances(
		Filters=[
		{
			'Name' : 'tag:Backup',
			'Values' : [
				'Yes',
			]
		}
		]
	)

	reslen = len(instance['Reservations']); r_count = 0

	while r_count < reslen:
		inslen = len(instance['Reservations'][r_count]['Instances'])
		i_count = 0
		while i_count < inslen:
			instance_id = instance['Reservations'][r_count]['Instances'][i_count]['InstanceId']
			instance_name = instance['Reservations'][r_count]['Instances'][i_count]['PrivateDnsName']
			execute_ec2_snapshot(instance_id,instance_name)
	
			i_count = i_count + 1
		r_count = r_count + 1

def lambda_handler(event, context):
        pull_ec2_details()
        return {
        }

lambda_handler("event","context")

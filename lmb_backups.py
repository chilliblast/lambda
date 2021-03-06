import boto3
import subprocess
import time

ec2 = boto3.client('ec2')

def execute_ec2_snapshot(instance_id,instance_name):
	global snapshot
	volumes = ec2.describe_instance_attribute(InstanceId=instance_id,Attribute='blockDeviceMapping')
	volen = len(volumes['BlockDeviceMappings'])
	for v_id in volumes['BlockDeviceMappings']:
		volume_id = v_id['Ebs']['VolumeId']
		start_time = time.strftime("%d%m%Y")

# We dont want to wait for each snapshot execution to complete
		snapshot = ec2.create_snapshot(
			Description=instance_name,
			VolumeId=volume_id,
			DryRun=False
		)

                print("Waiting for snapshot %s completion" % (snapshot['SnapshotId']))
                waiter = ec2.get_waiter('snapshot_completed')
                print("Snapshot %s successfully completed" % (snapshot['SnapshotId']))

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

### DEBUG
                print("Deleting snapshot %s " % (snapshot['SnapshotId']))
                delete_snapshot = ec2.delete_snapshot(
                        SnapshotId=snapshot['SnapshotId'],
                )
                print("Snapshot %s deleted" % (snapshot['SnapshotId']))
### DEBUG

def pull_ec2_details():
	global instance_id,instance_name
	c_time = time.localtime()
	print("Describe Instances Start time is: %s " % c_time)
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

### DEBUG
	print("Instance Raw Data is: %s" % (instance))
### DEBUG

	c_time = time.localtime()
	print("Describe Instances Finish time is: %s " % c_time)

	reslen = len(instance['Reservations']); r_count = 0

	c_time = time.localtime()
	print("Snapshot Creation Start time is: %s " % c_time)
	while r_count < reslen:
		inslen = len(instance['Reservations'][r_count]['Instances'])
		i_count = 0
		while i_count < inslen:
			instance_id = instance['Reservations'][r_count]['Instances'][i_count]['InstanceId']
			instance_name = instance['Reservations'][r_count]['Instances'][i_count]['PrivateDnsName']
			execute_ec2_snapshot(instance_id,instance_name)
	
			i_count = i_count + 1
		r_count = r_count + 1

	c_time = time.localtime()
        print("Snapshot Creation Finish time is: %s " % c_time)

def lambda_handler(event, context):
        pull_ec2_details()
        return {
        }

lambda_handler("event","context")

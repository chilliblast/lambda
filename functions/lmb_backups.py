#!/usr/bin/python

import boto3
import time

DAYS = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}

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
		print("Waiting for snapshot %s of instance %s to complete..." % (snapshot['SnapshotId'], instance_name)) 
		waiter = ec2.get_waiter('snapshot_completed')
		print("Snapshot %s completed for volume %s" % (snapshot['SnapshotId'], volume_id))
	
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

	for reservations in (instance["Reservations"]):
		for instance in (reservations["Instances"]):
			SS="No";DB="No"
			instance_id = instance['InstanceId'];instance_name = instance['PrivateDnsName']
			for tags in (instance["Tags"]):
				tgs_values = tags.values()
				if tgs_values[1] == "Backup" and tgs_values[0] == "Yes":
					SS = "Yes"
				if tgs_values[1] == "Backup_Schedule" and tgs_values[0] == "D":
					DB = "Yes"
			# Daily / Weekday Backups Only
### DEBUG
#			print("dotw var: %s" % (dotw))
#			print("SS var: %s" % (SS))
#			print("DB var: %s" % (DB))
### DEBUG

			if SS == "Yes" and DB == "Yes" and 0 < dotw > 6:
				execute_ec2_snapshot(instance_id,instance_name)
			else:
				print("Host %s does not require backups on weekday %s" % (instance_name, dotw))

def lambda_handler(event, context):
        pull_ec2_details()
        return {
        }

dotw = time.strftime("%w")
lambda_handler("event","context")

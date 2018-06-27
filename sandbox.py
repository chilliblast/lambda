#!/usr/bin/python
import boto3

# List available waiters
def get_instance_data():
	ec2 = boto3.client('ec2', region_name='eu-west-1')
#	print ec2.waiter_names

#	waiter = ec2.get_waiter('snapshot_completed')

	#

	instances = ec2.describe_instances(
		Filters=[
			{
				'Name' : 'tag:Backup',
				'Values' : [
				'Yes',
				]
			}
		]
	)

	for reservations in (instances["Reservations"]):
		for instance in (reservations["Instances"]):
			instance_id = instance['InstanceId']
			for tags in (instance["Tags"]):
#				print("tags variable contains: %s" % (tags))
				tgs_values = tags.values()
#				print(tgs_values)
#				print("tgs_values 0 is: %s" % (tgs_values[0]))
#				print("tgs_values 1 is: %s" % (tgs_values[1]))
				if tgs_values[1] == "Backup" and tgs_values[0] == "Yes":
					print("Instance %s to be backed up" % (instance_id))

get_instance_data()

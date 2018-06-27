#!/usr/bin/python
import boto3

# List available waiters
ec2 = boto3.client('ec2', region_name='eu-west-1')
print ec2.waiter_names

waiter = ec2.get_waiter('snapshot_completed')

#

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
print("RAW instance variable data is %s" % instance)
print("\n");print("\n");print("\n")
if "Backup" in instance['Reservations'][0]['Instances'][0]['Tags']:
	print("Backup stated")
print("\n");print("\n");print("\n")
print(instance['Reservations'][0]['Instances'][0]['Tags'])
print("\n");print("\n");print("\n")
print(instance['Reservations'][0]['Instances'][0]['Tags'][1])
tags = instance['Reservations'][0]['Instances'][0]['Tags']
print("Tags dictionary now contains: %s" % tags)
listlen = len(tags)
print("Tags list length is %d" % (listlen))
dictlen = len(tags[0])
print("Tags dictionary length is %d" % (dictlen))
tagsfind = tags[1].get('Backup',"not found")
print("Looking for specific value, did we find it? %s" % (tagsfind))
print("\n");print("\n");print("\n")
print(tags[1])

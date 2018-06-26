import boto3
import time

ec2 = boto3.client('ec2')

def execute_ec2_snapshot(instance_id,instance_name):
	global snapshot
	volumes = ec2.describe_instance_attribute(InstanceId=instance_id,Attribute='blockDeviceMapping')
	volen = len(volumes['BlockDeviceMappings'])
#	print("RAW volumes variable contains: ", volumes)
#	print("There are %i list items in volumes" % volen)
	for v_id in volumes['BlockDeviceMappings']:
#		print("Volume Entry is: ", v_id)
		volume_id = v_id['Ebs']['VolumeId']
#		print("Volume Id is: %s" % volume_id)
		start_time = time.strftime("%d%m%Y")
		snapshot = ec2.create_snapshot(
			Description=instance_name,
			VolumeId=volume_id,
			DryRun=False
		)
		print("Snapshot %s taken of volume %s" % (snapshot['SnapshotId'], volume_id))
	
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

instance = ec2.describe_instances(
        Filters=[
                {
                        'Name' : 'tag:Backup',
                        'Values' : [
                                'Nope',
                                        ]
                }
        ]
)
reslen = len(instance['Reservations']); r_count = 0
#print("RAW data is: ", instance)

while r_count < reslen:
	inslen = len(instance['Reservations'][r_count]['Instances'])
#	print("Instance List size is: ",inslen)
	i_count = 0
	while i_count < inslen:
#		print("i_count variable is: ", i_count)
		instance_name = instance['Reservations'][r_count]['Instances'][i_count]['PrivateDnsName']
#		print("instance name is: ", instance_name)
		instance_id = instance['Reservations'][r_count]['Instances'][i_count]['InstanceId']
#		print("instance id is: ", instance_id)
	
		execute_ec2_snapshot(instance_id,instance_name)

		i_count = i_count + 1
#	print("r_count variable is: ", r_count)
	r_count = r_count + 1

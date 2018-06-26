import boto3

ec2 = boto3.client('ec2')
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
	print("Instance List size is: ",inslen)
	i_count = 0
	while i_count < inslen:
		print("i_count variable is: ", i_count)
		instance_name = instance['Reservations'][r_count]['Instances'][i_count]['PrivateDnsName']
		print("instance name is: ", instance_name)
		instance_id = instance['Reservations'][r_count]['Instances'][i_count]['InstanceId']
		print("instance id is: ", instance_id)
		i_count = i_count + 1
	print("r_count variable is: ", r_count)
	r_count = r_count + 1

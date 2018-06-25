import boto3

ec2 = boto3.client('ec2')
instance = ec2.describe_instances(
	Filters=[
		{
			'Name' : 'tag:Backup',
			'Values' : [
				'yes',
					]
		}
	]
)
print(instance)

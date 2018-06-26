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
#print("Raw instance variable data is: ",instance)
instlen = len(instance['Reservations'])
print("Instance Length is ",instlen)

count = 0

while count < instlen:
        print("Count variable is: ", count)
        instance_name = instance['Reservations'][count]['Instances'][0]['PrivateDnsName']
        instance_id = instance['Reservations'][count]['Instances'][0]['InstanceId']
        print("Instance Name is: ",instance_name)
        print("Instance ID is: ",instance_id)
        count = count + 1

print("\n")
instlen = len(instance['Reservations'])
print("Number of items (instances) returned is: ",instlen)

import boto3

# List available waiters
ec2 = boto3.client('ec2', region_name='eu-west-1')
print ec2.waiter_names

waiter = ec2.get_waiter('snapshot_completed')

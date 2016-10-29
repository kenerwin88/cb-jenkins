import boto3
import sys

# Variables
access_key = sys.argv[1]
secret_access_key = sys.argv[2]
region = sys.argv[3]
security_group_name = 'Coinbase-SG01'
core_os_ami = sys.argv[4]
instance_name = 'Coinbase-WEB01-Test'
keypair_name = sys.argv[5]

# Connect to AWS
client = boto3.client('ec2', aws_access_key_id=access_key,
                      aws_secret_access_key=secret_access_key,
                      region_name=region)
ec2 = boto3.resource('ec2', aws_access_key_id=access_key,
                     aws_secret_access_key=secret_access_key,
                     region_name=region)

# Create Security Group
security_groups = client.describe_security_groups()
group_found = False
for group in security_groups['SecurityGroups']:
    if group['GroupName'] == security_group_name:
        group_found = group
        print 'Security Group already exists, skipping.'
if not group_found:
    print 'Creating Security Group...'
    group = client.create_security_group(GroupName=security_group_name,
                                         Description='Web Security Group')
    sec_group = ec2.SecurityGroup(group['GroupId'])
    sec_group.authorize_ingress(IpProtocol='TCP',
                                FromPort=80,
                                ToPort=80,
                                CidrIp='0.0.0.0/0',
                                GroupName=security_group_name)
    sec_group.authorize_ingress(IpProtocol='TCP',
                                FromPort=22,
                                ToPort=22,
                                CidrIp='0.0.0.0/0',
                                GroupName=security_group_name)
    print 'Security Group Created!'

# Spin up CoreOS Instance
print 'Spinning up new CoreOS instance.'

# Userdata
userdata = """#cloud-config
hostname: "coreos"
coreos:
  units:
    - name: "cbweb.service"
      command: "start"
      content: |
        [Unit]
        Description=CBWeb
        Author=Ken Erwin
        After=docker.service

        [Service]
        Restart=always
        ExecStart=/usr/bin/docker run -p 80:80 --name cbweb kenerwin88/cbweb
        ExecStop=/usr/bin/docker stop -t 2 cbweb
"""

instance = ec2.create_instances(ImageId=core_os_ami,
                                MinCount=1,
                                MaxCount=1,
                                InstanceType='t2.micro',
                                SecurityGroups=[security_group_name],
                                KeyName=keypair_name,
                                UserData=userdata)

instance[0].create_tags(Tags=[{'Key': 'Name',
                               'Value': instance_name}])
print 'Instance started!'

ip = instance[0].public_ip_address
url = "http://" + str(ip)
print "Page will be available at: %s within a few minutes." % url

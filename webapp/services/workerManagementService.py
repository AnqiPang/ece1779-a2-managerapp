import time
import boto3
from flask import current_app
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, FloatField
from wtforms.validators import NumberRange, DataRequired
from webapp.repository import workerManagementRepo


class AutoScalingPolicyForm(FlaskForm):
    thresholdForGrowing = IntegerField('CPU threshold for growing the pool',
                                       validators=[NumberRange(min=0, max=100)])
    thresholdForShrinking = IntegerField('CPU threshold for shrinking the pool',
                                         validators=[NumberRange(min=0, max=100)])
    ratioToGrowing = FloatField('Ratio to expand the pool', validators=[NumberRange(min=0, max=10)])
    ratioToShrinking = FloatField('Ratio to shrink the pool', validators=[NumberRange(min=0, max=10)])
    submit = SubmitField('Submit')


class WorkerManagementService:
    EC2 = boto3.client('ec2')
    ELB = boto3.client('elbv2')
    S3 = boto3.client('s3')

    def create_new_instance(self):
        response = self.EC2.run_instances(
            ImageId=current_app.config["AMI_ID"],
            Monitoring={'Enabled': True},
            Placement={'AvailabilityZone': current_app.config["ZONE"]},
            InstanceType=current_app.config["INSTANCE_TYPE"],
            MinCount=1,
            MaxCount=1,
            UserData = current_app.config["USERDATA"],
            KeyName=current_app.config["KEYNAME"],
            SubnetId=current_app.config["SUBNETID"],
            SecurityGroupIds=current_app.config["SG"],
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': current_app.config["EC2NAME"]
                        },
                    ]
                 },
            ],
        )
        for instance in response['Instances']:
            print(instance['InstanceId'] + " created!")
        return response['Instances'][0]['InstanceId']

    def get_stopped_instances(self):
        ec2_filter = [{'Name': 'tag:Name', 'Values': [current_app.config["EC2NAME"]]},
                      {'Name': 'instance-state-name', 'Values': ['stopped']}]
        return self.EC2.describe_instances(Filters=ec2_filter)

    def register_target(self, instance_id):
        target_group=current_app.config["TARGET_GROUP_ARN"]
        target = [{'Id': instance_id,
                   'Port': 5000}]
        self.ELB.register_targets(TargetGroupArn = target_group, Targets = target)

    def start_instance(self, instance_id):
        self.EC2.start_instances(InstanceIds=[instance_id])

    def grow_one_worker(self):
        target_instance_id = self.get_target_instance()
        error = False
        if len(target_instance_id) >= 10:
            error = True
            return [error, 'The maximum size of the worker pool is 10!']
        stopped_instances = self.get_stopped_instances()['Reservations']
        if stopped_instances:
            new_instance_id = stopped_instances[0]['Instances'][0]['InstanceId']
            self.start_instance(new_instance_id)
        else: #create a new instance
            new_instance_id = self.create_new_instance()
        status = self.EC2.describe_instance_status(InstanceIds=[new_instance_id])
        while len(status['InstanceStatuses']) < 1:
            time.sleep(1)
            status = self.EC2.describe_instance_status(InstanceIds=[new_instance_id])
        while status['InstanceStatuses'][0]['InstanceState']['Name'] != 'running':
            time.sleep(1)
            status = self.EC2.describe_instance_status(InstanceIds=[new_instance_id])
        self.register_target(new_instance_id)
        return [error, '']

    def get_target_instance(self):
        target_group = self.ELB.describe_target_health(TargetGroupArn=current_app.config["TARGET_GROUP_ARN"])
        instances_id = []
        if target_group['TargetHealthDescriptions']:
            for target in target_group['TargetHealthDescriptions']:
                if target['TargetHealth']['State'] != 'draining':
                    instances_id.append(target['Target']['Id'])
        return instances_id

    def deregister_target(self, instance_id):
        target_group = current_app.config["TARGET_GROUP_ARN"]
        target = [{'Id': instance_id}]
        self.ELB.deregister_targets(TargetGroupArn=target_group,
                                    Targets=target)

    def stop_instance(self, instance_id):
        self.EC2.stop_instances(InstanceIds=[instance_id], Hibernate=False, Force=False)

    def terminate_instance(self, instance_id):
        self.EC2.terminate_instances(InstanceIds=[instance_id])

    def shrink_one_worker(self):
        target_instance_id = self.get_target_instance()
        error = False
        if len(target_instance_id) <= 1:
            error = True
            return [error, 'The minimum size of the worker pool is 1!']
        else:
            self.deregister_target(target_instance_id[0])
            self.stop_instance(target_instance_id[0])
            return [error, '']

    def terminate_all_instance(self):
        ins = self.EC2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [current_app.config["EC2NAME"]]}])['Reservations']
        if ins:
            targets = []
            for res in ins:
                targets.append(res['Instances'][0]['InstanceId'])
            for target_id in targets:
                self.deregister_target(target_id)
                self.terminate_instance(target_id)

    def stop_manager(self):
        self.terminate_all_instance()
        manager_filter = [{'Name': 'tag:Name', 'Values': [current_app.config["MANAGER_NAME"]]}]
        manager = self.EC2.describe_instances(Filters=manager_filter)['Reservations']
        if manager:
            manager_id = manager[0]['Instances'][0]['InstanceId']
            workerManagementRepo.init_current_instance_amount(0)
            self.stop_instance(manager_id)

    def init_current_instance_amount(self):
        workerManagementRepo.init_current_instance_amount(len(self.get_target_instance()))

    def update_management_data(self, threshold_growing, threshold_shrinking, ratio_growing, ratio_shrinking):
        workerManagementRepo.update_management_data(threshold_growing, threshold_shrinking, ratio_growing,
                                                    ratio_shrinking)

    def delete_s3_app_data(self):
        error = False
        if 'Contents' in self.S3.list_objects(Bucket=current_app.config['S3_BUCKET']):
            for item in self.S3.list_objects(Bucket=current_app.config['S3_BUCKET'])['Contents']:
                self.S3.delete_objects(
                    Bucket=current_app.config['S3_BUCKET'],
                    Delete={
                        'Objects': [
                            {
                                'Key': item['Key'],
                            },
                        ],
                        'Quiet': True
                    },
                )
            return [error, '']
        else:
            error = True
            return [error, 'There is no application data to delete!']
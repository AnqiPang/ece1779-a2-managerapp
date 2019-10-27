from flask import current_app
import json
import base64
from webapp.requestTemplates.cloudWatchRequest import *
import boto3


class WorkListService:
    # CLIENT = boto3.client('elbv2', aws_access_key_id=current_app.config["AWS_ACCESS_KEY_ID"],
    #                       aws_secret_access_key=current_app.config["AWS_SECRET_ACCESS_KEY"])
    #
    # TARGET_GROUP = CLIENT.describe_target_health(
    #   TargetGroupArn=current_app.config["TARGET_GROUP_ARN"])
    #
    # CLOUD_WATCH = boto3.client("cloudwatch", aws_access_key_id=current_app.config["AWS_ACCESS_KEY_ID"],
    #                            aws_secret_access_key=current_app.config["AWS_SECRET_ACCESS_KEY"])

    CLIENT = boto3.client('elbv2')

    TARGET_GROUP = CLIENT.describe_target_health(
      TargetGroupArn=current_app.config["TARGET_GROUP_ARN"])

    CLOUD_WATCH = boto3.client("cloudwatch")

    def get_instances_cpu_matrix_images(self):
        charts = []
        for target in self.TARGET_GROUP['TargetHealthDescriptions']:
            instance_id = target['Target']['Id']
            CPUUtilization_REQUEST["metrics"][0][3] = instance_id
            response = self.CLOUD_WATCH.get_metric_widget_image(MetricWidget=json.dumps(CPUUtilization_REQUEST))
            image = base64.b64encode(response['MetricWidgetImage']).decode("utf-8")
            chart = [instance_id, image]
            charts.append(chart)
        return charts

from flask import current_app
import json
import base64
from webapp.requestTemplates.cpuRequest import *
from webapp.requestTemplates.networkPacketsInRequest import *
import boto3


class WorkListService:
    CLIENT = boto3.client('elbv2')
    CLOUD_WATCH = boto3.client("cloudwatch")

    def get_charts(self):
        target_group = self.CLIENT.describe_target_health(TargetGroupArn=current_app.config["TARGET_GROUP_ARN"])
        cpu_charts = []
        networkin_charts = []
        instances = []
        for target in target_group['TargetHealthDescriptions']:
            instance_id = target['Target']['Id']
            instances.append(instance_id)

            CPUUtilization_REQUEST["metrics"][0][3] = instance_id
            cpu_response = self.CLOUD_WATCH.get_metric_widget_image(MetricWidget=json.dumps(CPUUtilization_REQUEST))
            cpu_chart = base64.b64encode(cpu_response['MetricWidgetImage']).decode("utf-8")
            cpu_charts.append(cpu_chart)

            NETWORK_PACKETS_IN_REQUEST["metrics"][0][3] = instance_id
            networkin_response = self.CLOUD_WATCH.get_metric_widget_image(MetricWidget=json.dumps(NETWORK_PACKETS_IN_REQUEST))
            networkin_chart = base64.b64encode(networkin_response['MetricWidgetImage']).decode("utf-8")
            networkin_charts.append(networkin_chart)

        return instances, cpu_charts, networkin_charts

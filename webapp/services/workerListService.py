from flask import current_app
import json
import base64
from webapp.requestTemplates.cpuRequest import *
from webapp.requestTemplates.networkPacketsInRequest import *
import boto3
from webapp.requestTemplates.requestcount import *


class WorkListService:
    CLIENT = boto3.client('elbv2')
    CLOUD_WATCH = boto3.client("cloudwatch")

    def get_charts(self):
        target_group = self.CLIENT.describe_target_health(TargetGroupArn=current_app.config["TARGET_GROUP_ARN"])
        cpu_charts = []
        RequestCount_in_charts = []
        instances = []
        for target in target_group['TargetHealthDescriptions']:
            if target['TargetHealth']['State'] != 'draining':
                instance_id = target['Target']['Id']
                instances.append(instance_id)

                CPUUtilization_REQUEST["metrics"][0][3] = instance_id
                cpu_response = self.CLOUD_WATCH.get_metric_widget_image(MetricWidget=json.dumps(CPUUtilization_REQUEST))
                cpu_chart = base64.b64encode(cpu_response['MetricWidgetImage']).decode("utf-8")
                cpu_charts.append(cpu_chart)

                # Hidden
                # NETWORK_PACKETS_IN_REQUEST["metrics"][0][3] = instance_id
                # network_packets_in_response = self.CLOUD_WATCH.get_metric_widget_image(
                # MetricWidget=json.dumps(NETWORK_PACKETS_IN_REQUEST))
                # network_packet_in_chart = base64.b64encode(network_packets_in_response['MetricWidgetImage']).decode("utf-8")
                # network_packets_in_charts.append(network_packet_in_chart)

                #LoadBalancer RequestCount
                #RequestCount_IN_REQUEST["metrics"][0][3] = instance_id
                RequestCount_in_response = self.CLOUD_WATCH.get_metric_widget_image(
                MetricWidget=json.dumps(RequestCount_IN_REQUEST))
                RequestCount_in_chart = base64.b64encode(RequestCount_in_response['MetricWidgetImage']).decode("utf-8")
                RequestCount_in_charts.append(RequestCount_in_chart)
        return instances, cpu_charts, RequestCount_in_charts

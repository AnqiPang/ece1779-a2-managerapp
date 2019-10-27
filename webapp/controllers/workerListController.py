from flask import Blueprint, render_template, current_app
import boto3
import json
import base64
from webapp.requestTemplates.cloudWatchRequest import *


workerList = Blueprint('workerList', __name__)


@workerList.route("/workers", methods=["GET"])
def list_worker():
    client = boto3.client('elbv2', aws_access_key_id=current_app.config["AWS_ACCESS_KEY_ID"],
                          aws_secret_access_key=current_app.config["AWS_SECRET_ACCESS_KEY"])
    # print(client.describe_target_groups(
    #   LoadBalancerArn=
    #   "arn:aws:elasticloadbalancing:us-east-1:935290738939:loadbalancer/app/ECE1779A2-LB/795b2b8a99d5ef5f"))

    target_group = client.describe_target_health(
      TargetGroupArn=current_app.config["TARGET_GROUP_ARN"])

    cloud_watch = boto3.client("cloudwatch", aws_access_key_id=current_app.config["AWS_ACCESS_KEY_ID"],
                               aws_secret_access_key=current_app.config["AWS_SECRET_ACCESS_KEY"])
    instances = []
    for target in target_group['TargetHealthDescriptions']:
        instances.append(target['Target']['Id'])

    charts = []
    for i in instances:
        CPUUtilization_REQUEST["metrics"][0][3] = i
        response = cloud_watch.get_metric_widget_image(MetricWidget=json.dumps(CPUUtilization_REQUEST))
        image = base64.b64encode(response['MetricWidgetImage']).decode("utf-8")
        chart = [i, image]
        charts.append(chart)

    return render_template("workerList.html", charts=charts)

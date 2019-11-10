from flask import Blueprint, render_template
from webapp.services.workerListService import *


workerList = Blueprint('workerList', __name__)


@workerList.route("/workers", methods=["GET"])
def list_worker():
    work_list_service = WorkListService()
    instances, cpu_charts, requests_charts = work_list_service.get_charts()
    instance, cpu_chart, request_chart = work_list_service.get_chart()

    return render_template("workerList.html", charts=zip(instances, cpu_charts, requests_charts), manager_chart = zip(instance, cpu_chart, request_chart))

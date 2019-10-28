from flask import Blueprint, render_template
from webapp.services.workerListService import *


workerList = Blueprint('workerList', __name__)


@workerList.route("/workers", methods=["GET"])
def list_worker():
    work_list_service = WorkListService()
    instances, cpu_charts, network_packets_in_charts = work_list_service.get_charts()

    return render_template("workerList.html", charts=zip(instances, cpu_charts, network_packets_in_charts))

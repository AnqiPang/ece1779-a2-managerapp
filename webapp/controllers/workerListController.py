from flask import Blueprint, render_template
from webapp.services.workerListService import *


workerList = Blueprint('workerList', __name__)


@workerList.route("/workers", methods=["GET"])
def list_worker():
    work_list_service = WorkListService()
    charts = work_list_service.get_instances_cpu_matrix_images()

    return render_template("workerList.html", charts=charts)

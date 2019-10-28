from flask import Blueprint, render_template, request, current_app
from webapp.services.workerManagementService import *


workerManagement = Blueprint('workerManagement', __name__)

WORKER_MANAGEMENT_PAGE = "workerManagement.html"
INTERNAL_ERROR_MSG = "Internal Error, please try again later."


@workerManagement.route("/workers/management", methods=["GET", "POST"])
def manage_worker():
    form = AutoScalingPolicyForm()
    if form.validate_on_submit():
        worker_management_service = WorkerManagementService()
        worker_management_service.save_management_data(form.thresholdForGrowing.data, form.thresholdForShrinking.data,
                                                       form.ratioToGrowing.data, form.ratioToShrinking.data)
    else:
        if request.method == 'POST':
            current_app.logger.error("----------Internal Error: {}----------".format(form.errors))
            return render_template(WORKER_MANAGEMENT_PAGE, form=form, error=INTERNAL_ERROR_MSG), 500
    return render_template(WORKER_MANAGEMENT_PAGE, form=form)

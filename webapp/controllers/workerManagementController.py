from flask import Blueprint, render_template, request, current_app
from webapp.services.workerManagementService import *


workerManagement = Blueprint('workerManagement', __name__)

WORKER_MANAGEMENT_PAGE = "workerManagement.html"
INTERNAL_ERROR_MSG = "Internal Error, please try again later."
AUTO_SCALING_POLICY_CHANGE_SUCCESS_MSG = "Auto-scaling policy has been changed successfully!"
GROW_ONE_WORKER_SUCCESS_MSG = "Worker pool size has growed by 1 successfully!"
SHRINK_ONE_WORKER_SUCCESS_MSG = "Worker pool size has shrinked by 1 successfully!"


@workerManagement.route("/workers/management", methods=["GET", "POST"])
def manage_worker():
    form = AutoScalingPolicyForm()
    if form.validate_on_submit():
        worker_management_service = WorkerManagementService()
        worker_management_service.update_management_data(form.thresholdForGrowing.data, form.thresholdForShrinking.data,
                                                       form.ratioToGrowing.data, form.ratioToShrinking.data)
        current_app.logger.info("----------{}----------".format(AUTO_SCALING_POLICY_CHANGE_SUCCESS_MSG))
        return render_template(WORKER_MANAGEMENT_PAGE, form=form, message=AUTO_SCALING_POLICY_CHANGE_SUCCESS_MSG)
    else:
        if request.method == 'POST':
            current_app.logger.error("----------Internal Error: {}----------".format(form.errors))
            return render_template(WORKER_MANAGEMENT_PAGE, form=form, error=INTERNAL_ERROR_MSG), 500
    return render_template(WORKER_MANAGEMENT_PAGE, form=form)

@workerManagement.route("/workers/grow_one", method=["GET", "POST"])
def grow_onw_worker():
    worker_management_service = WorkerManagementService()
    worker_management_service.grow_one_worker()
    return render_template(WORKER_MANAGEMENT_PAGE, message=GROW_ONE_WORKER_SUCCESS_MSG)

from flask import Blueprint, render_template, request, current_app, redirect, url_for
from webapp.services.workerManagementService import *

workerManagement = Blueprint('workerManagement', __name__)

WORKER_MANAGEMENT_PAGE = "workerManagement.html"
INTERNAL_ERROR_MSG = "Internal Error, please try again later."
AUTO_SCALING_POLICY_CHANGE_SUCCESS_MSG = "Auto-scaling policy has been changed successfully!"
GROW_ONE_WORKER_SUCCESS_MSG = "Worker pool size has grown by 1 successfully!"
SHRINK_ONE_WORKER_SUCCESS_MSG = "Worker pool size has shrunk by 1 successfully!"
STOP_MANAGER_SUCCESS_MSG = "Manager has been stopped successfully!"
CLEAR_S3_SUCCESS_MSG = "application app data has been deleted successfully!"


@workerManagement.route("/workers/management", methods=["GET", "POST"])
def manage_worker():
    worker_management_service = WorkerManagementService()
    worker_management_service.init_current_instance_amount()
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
    message = request.args.get('message')
    error = request.args.get('error')
    if message:
        return render_template(WORKER_MANAGEMENT_PAGE, form=form, message=message)
    elif error:
        return render_template(WORKER_MANAGEMENT_PAGE, form=form, error=error)
    else:
        return render_template(WORKER_MANAGEMENT_PAGE, form=form)


@workerManagement.route("/workers/grow_one")
def grow_one_worker():
    worker_management_service = WorkerManagementService()
    [error, msg] = worker_management_service.grow_one_worker()
    if error:
        return redirect(url_for('workerManagement.manage_worker', error=msg))
    else:
        return redirect(url_for('workerManagement.manage_worker', message=GROW_ONE_WORKER_SUCCESS_MSG))


@workerManagement.route("/workers/shrink_one")
def shrink_one_worker():
    worker_management_service = WorkerManagementService()
    [error, msg] = worker_management_service.shrink_one_worker()
    if error:
        return redirect(url_for('workerManagement.manage_worker', error=msg))
    else:
        return redirect(url_for('workerManagement.manage_worker', message=SHRINK_ONE_WORKER_SUCCESS_MSG))

@workerManagement.route("/workers/stop_manager")
def stop_manager():
    worker_management_service = WorkerManagementService()
    worker_management_service.stop_manager()
    return redirect(url_for('workerManagement.manage_worker', message=STOP_MANAGER_SUCCESS_MSG))

@workerManagement.route("/workers/clear_s3")
def clear_s3():
    worker_management_service = WorkerManagementService()
    worker_management_service.delete_s3_app_data()
    worker_management_service.delete_rds_data()
    return redirect(url_for('workerManagement.manage_worker', message=CLEAR_S3_SUCCESS_MSG))
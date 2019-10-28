from flask import Blueprint, render_template
from webapp.services import workerManagementService


workerManagement = Blueprint('workerManagement', __name__)


@workerManagement.route("/workers/management", methods=["GET"])
def manage_worker():
    auto_scaling_policy_form = workerManagementService.AutoScalingPolicyForm()
    return render_template("workerManagement.html", form=auto_scaling_policy_form)

from flask import Blueprint, render_template


workerManagement = Blueprint('workerManagement', __name__)


@workerManagement.route("/workers/management", methods=["GET"])
def manage_worker():
    return render_template("workerManagement.html")

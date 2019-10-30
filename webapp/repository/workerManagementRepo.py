from webapp.models.workerManagement import *
from webapp.models.scriptMonitor import *


def update_management_data(threshold_growing, threshold_shrinking, ratio_growing, ratio_shrinking):
    record = WorkerManagement.query.get(1)
    if record is None:
        data = WorkerManagement(threshold_growing, threshold_shrinking, ratio_growing, ratio_shrinking)
        db.session.add(data)
    else:
        record.threshold_growing = threshold_growing
        record.threshold_shrinking = threshold_shrinking
        record.ratio_growing = ratio_growing
        record.ratio_shrinking = ratio_shrinking
    db.session.commit()


def init_current_instance_amount(current_instance_amount):
    record = ScriptMonitor.query.get(1)
    if record is None:
        data = ScriptMonitor(current_instance_amount, 5)
        db.session.add(data)
    else:
        record.current_instance_amount = current_instance_amount
        record.retry_time = 5
    db.session.commit()

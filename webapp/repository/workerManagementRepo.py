from webapp.models.base import db
from webapp.models.workerManagement import *


def save_management_data(threshold_growing, threshold_shrinking, ratio_growing, ratio_shrinking):
    data = WorkerManagement(threshold_growing, threshold_shrinking, ratio_growing, ratio_shrinking)
    db.session.add(data)
    db.session.commit()

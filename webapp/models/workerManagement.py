from .base import db


class WorkerManagement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    threshold_growing = db.Column(db.INTEGER, nullable=False)
    threshold_shrinking = db.Column(db.INTEGER, nullable=False)
    ratio_growing = db.Column(db.FLOAT(precision='3,2'), nullable=False)
    ratio_shrinking = db.Column(db.FLOAT(precision='3,2'), nullable=False)

    def __init__(self, threshold_growing, threshold_shrinking, ratio_growing, ratio_shrinking):
        self.threshold_growing = threshold_growing
        self.threshold_shrinking = threshold_shrinking
        self.ratio_growing = ratio_growing
        self.ratio_shrinking = ratio_shrinking


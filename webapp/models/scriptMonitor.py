from .base import db


class ScriptMonitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    current_instance_amount = db.Column(db.INTEGER)
    retry_time = db.Column(db.INTEGER)

    def __init__(self, current_instance_amount, retry_time):
        self.current_instance_amount = current_instance_amount
        self.retry_time = retry_time

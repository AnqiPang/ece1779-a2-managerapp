from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, FloatField
from wtforms.validators import NumberRange, DataRequired
from webapp.repository import workerManagementRepo


class AutoScalingPolicyForm(FlaskForm):
    thresholdForGrowing = IntegerField('CPU threshold for growing the pool',
                                       validators=[NumberRange(min=0, max=100)])
    thresholdForShrinking = IntegerField('CPU threshold for shrinking the pool',
                                       validators=[NumberRange(min=0, max=100)])
    ratioToGrowing = FloatField('Ratio to expand the pool', validators=[NumberRange(min=0, max=10)])
    ratioToShrinking = FloatField('Ratio to shrink the pool', validators=[NumberRange(min=0, max=10)])
    submit = SubmitField('Submit')


class WorkerManagementService:
    def update_management_data(self, threshold_growing, threshold_shrinking, ratio_growing, ratio_shrinking):
        workerManagementRepo.update_management_data(threshold_growing, threshold_shrinking, ratio_growing, ratio_shrinking)







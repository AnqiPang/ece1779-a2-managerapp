from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length
from webapp.repository import workerManagementRepo


class AutoScalingPolicyForm(FlaskForm):
    thresholdForGrowing = IntegerField('CPU threshold for growing the pool',
                                       validators=[DataRequired(), Length(min=0, max=100)])
    thresholdForShrinking = IntegerField('CPU threshold for shrinking the pool',
                                       validators=[DataRequired(), Length(min=0, max=100)])
    ratioToGrowing = FloatField('Ratio to expand the pool',
                                       validators=[DataRequired(), Length(min=0, max=10)])
    ratioToShrinking = FloatField('Ratio to shrink the pool',
                                       validators=[DataRequired(), Length(min=0, max=10)])
    submit = SubmitField('Submit')

class WorkerManagementService:
    def save_management_data(self, threshold_growing, threshold_shrinking, ratio_growing, ratio_shrinking):
        workerManagementRepo.save_management_data(threshold_growing, threshold_shrinking, ratio_growing, ratio_shrinking)







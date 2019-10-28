from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length


class AutoScalingPolicyForm(FlaskForm):
    thresholdForGrowing = IntegerField('CPU threshold for growing the pool',
                                       validators=[DataRequired(), Length(min=0, max=100)])
    thresholdForShrinking = IntegerField('CPU threshold for shrinking the pool',
                                       validators=[DataRequired(), Length(min=0, max=100)])
    ratioToGrowing = IntegerField('Ratio to expand the pool',
                                       validators=[DataRequired(), Length(min=0, max=10)])
    ratioToShrinking = IntegerField('Ratio to shrink the pool',
                                       validators=[DataRequired(), Length(min=0, max=10)])
    submit = SubmitField('Submit')

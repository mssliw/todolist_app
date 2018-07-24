from flask_wtf import FlaskForm
from wtforms_alchemy import ModelForm

from models import TaskList, TaskCard, TaskDetails


class CreateListForm(ModelForm, FlaskForm):
    class Meta:
        model = TaskList


class AddCardForm(ModelForm, FlaskForm):
    class Meta:
        model = TaskCard


class AddDetailsForm(ModelForm, FlaskForm):
    class Meta:
        model = TaskDetails

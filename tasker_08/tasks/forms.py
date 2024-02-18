from django import forms
from . import models


class DateInput(forms.DateInput):
    input_type = 'date'


class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ('name', 'project', 'description', 'deadline', 'is_done' )
        widgets = {
            'deadline': DateInput,
        }

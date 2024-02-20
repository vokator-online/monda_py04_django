from django import forms
from django_select2 import forms as s2forms
from django.contrib.auth import get_user_model
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

class OwnerWidget(s2forms.ModelSelect2Widget):
    search_fields = (
        'username__icontains', 
        'last_name__icontains', 
        'email__icontains',
    )

class ProjectWidget(s2forms.ModelSelect2Widget):
    search_fields = (
        'name__icontains',
    )


class TaskSearchForm(forms.Form):
    project = forms.ModelChoiceField(
        queryset=models.Project.objects.all(),
        widget=ProjectWidget, 
        required=False,
    )
    owner = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        widget=OwnerWidget,
        required=False
    )

from django import forms
from django.core.validators import validate_email
from . import models


class TicketFormGuest(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['subject', 'body', 'sender_name', 'sender_email']

    def clean_sender_name(self):
        data = self.cleaned_data["sender_name"]
        if not data or not len(data) > 0:
            raise forms.ValidationError("please enter your full name")
        return data
    
    def clean_sender_email(self):
        data = self.cleaned_data["sender_email"]
        validate_email(data)
        return data


class TicketFormUser(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['subject', 'body']

from django import forms
from .models import Notifications, SeasonAlert



class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notifications
        fields = ['title',  'notification_type','message']


class SeasonAlertForm(forms.ModelForm):
    class Meta:
        model = SeasonAlert
        fields = ['user', 'notification', 'season'] 
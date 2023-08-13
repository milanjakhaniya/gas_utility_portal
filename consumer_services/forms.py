from django import forms
from .models import ServiceRequest, UserProfile
from django.contrib.auth.models import User

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['request_title', 'service_request_type', 'details', 'attachment']

class RequestTrackingForm(forms.Form):
    request_id = forms.CharField(max_length=100)

class RequestStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['request_id', 'request_status']
        widgets = {'request_id': forms.HiddenInput()}


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


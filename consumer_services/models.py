import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class ServiceRequest(models.Model):
    class ServiceRequestStatus(models.TextChoices):
        IN_PROGRESS = 'In Progress', _('in_progress')
        RESOLVED = 'Resolved', _('resolved')

    class ServiceRequestType(models.TextChoices):
        GAS_CYLINDER_DELIVERY = 'Gas Cylinder Delivery', _('Gas Cylinder Delivery')
        GAS_LEAKAGE_COMPLAINT = 'Gas Leakage Complaint', _('Gas Leakage Complaint')
        CHANGE_OF_CONTACT_DETAILS = 'Change of Contact Details', _('Change of Contact Details')
        PAYMENT_RELETED_ISSUE = 'Payment Related Issues', _('Payment Related Issues')

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    request_id = models.CharField(max_length=50, default=uuid.uuid4())
    request_title = models.CharField(max_length=100)
    request_status = models.CharField(
        max_length=50,
        choices=ServiceRequestStatus.choices,
        default=ServiceRequestStatus.IN_PROGRESS,
    )
    service_request_type = models.CharField(
        max_length=50,
        choices=ServiceRequestType.choices,
        default=ServiceRequestType.GAS_CYLINDER_DELIVERY,
    )
    details = models.TextField()
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
    submission_date = models.DateTimeField(null=True, blank=True)
    resolution_date = models.DateTimeField(null=True, blank=True)
    

class UserProfile(models.Model):
    class UserType(models.TextChoices):
        USER = 'us', _('user')
        REPRESENTATIVE = 'rp', _('representative')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(
        max_length=2,
        choices=UserType.choices,
        default=UserType.USER,
    )

    # Add additional customer profile fields here

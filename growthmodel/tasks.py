import string
from growthmodel.models import GrowthModelActivity
from celery import shared_task

 @shared_task
 def send_growthmodel_activity_alert_email():
    pass

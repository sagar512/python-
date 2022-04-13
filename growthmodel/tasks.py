from growthmodel.models import GrowthModel, GrowthModelActivity
from account.models import Users
from celery import shared_task
from rtf.utils import send_an_email
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.template.loader import render_to_string
from rtf.celery import app
from django.conf import settings

@shared_task
def send_growthmodel_activity_alert_email():
    start_date = (timezone.now() + timedelta(days=1)).date()
    end_date = (timezone.now() + timedelta(days=1)).date()

    growthModelActivityObjs = GrowthModelActivity.objects.exclude(Q(alert=False) | 
        Q(start_date__isnull=True) | Q(end_date__isnull=True)).filter(
        end_date__range=(start_date, end_date)).distinct()

    growthModelObjs = GrowthModel.objects.exclude(user_id__isnull=True).distinct()
    userObjs = Users.objects.exclude(email__isnull=True).distinct()

    for growthModelActivityObj in growthModelActivityObjs:
        user_id = growthModelObjs.filter(
            id=growthModelActivityObj.growthmodel_id).first().user_id
        userObj = userObjs.filter(id=user_id).first()

        if userObj:
            # Send an activity alert email
            subject = "Growth Model Actvity Alert"
            message_body = render_to_string(
                'growthmodel/growth_model_activity_alert.html', {
                    'activity_type': growthModelActivityObj.activity_type,
                    'activity_title': growthModelActivityObj.activity_title,
                    'activity_link': growthModelActivityObj.activity_link,
                    'user_name': userObj.first_name,
                }
            )
            from_email = f'YLIWAY Team <{settings.DEFAULT_FROM_EMAIL}>'
            recipient_list = [userObj.email,]
            send_an_email(subject, message_body, recipient_list, from_email)

    return True

@app.task
def add(x, y):
    z = x + y
    print(z)
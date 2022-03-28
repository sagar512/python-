from growthmodel.models import GrowthModelActivity
from celery import shared_task
from rtf.utils import send_an_email
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.template.loader import render_to_string

@shared_task
def send_growthmodel_activity_alert_email():
    start_date = timezone.now() + timedelta(days=1)
    end_date = timezone.now() + timedelta(days=1)

    growthmodel_ids = list(GrowthModelActivity.objects.exclude(Q(alert=False) | 
        Q(start_date__isnull=True) | Q(end_date__isnull=True)).filter(
        end_date__range=(start_date, end_date)).values_list('growth_model_id', flat=True))

    growthmodelObjs = GrowthModel.objects.exclude(user_id__isnull=True)

    for growthmodel_id in growthmodel_ids:
        userObj = Users.objects.filter(id=growthmodelObjs.get(
            id=growthmodel_id).user_id)

        # Send an activity alert email
        subject = "Growth Model Actvity Alert"
        message_body = render_to_string(
            'growthmodel/growth_model_activity_alert.html', {})
        from_email = ""
        recipient_list = [userObj.email,]
        send_an_email(subject, message_body, recipient_list, from_email)

    return True

            
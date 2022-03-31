import os
from celery import Celery
from celery.schedules import crontab

# setting the Django settings module.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rtf.settings')
app = Celery('rtf')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    # Executes daily at midnight.
    'send-growthmodel-activity-alert-email': {
        'task': 'growthmodel.tasks.send_growthmodel_activity_alert_email',
        'schedule': crontab(hour=0, minute=0),
        'args': (16, 16),
    },
}

# Looks up for task modules in Django applications and loads them
app.autodiscover_tasks()
import os
from celery import Celery
from celery.schedules import crontab

# setting the Django settings module.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rtf.settings')
app = Celery('rtf')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    # Executes daily at midnight.
    'add-every-monday-morning': {
        'task': 'growthmodel.tasks.add',
        # 'schedule': crontab(hour=0, minute=0),
        'schedule': crontab(minute='*/1'),
        'args': (16, 16),
    },
}

# Looks up for task modules in Django applications and loads them
app.autodiscover_tasks()
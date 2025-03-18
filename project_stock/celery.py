import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_stock.settings')

app = Celery('project_stock')
app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "update-stock-data-every-1-minutes": {
        "task": "stock_app.tasks.update_stock_data",
        "schedule": crontab(minute="*/1"),  
    },
}
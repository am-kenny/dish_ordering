import os

from celery import Celery

celery = Celery("celery_task", broker=f"pyamqp://guest@{os.environ.get('rabbit_host', 'localhost')}//")


@celery.task
def send_email(email):
    print("sent email to " + email)

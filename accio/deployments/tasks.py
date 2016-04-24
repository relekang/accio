from celery import shared_task
from django.utils import timezone


@shared_task
def deploy(deployment_id):
    from .models import Deployment
    deployment = Deployment.objects.get(pk=deployment_id)
    deployment.started_at = timezone.now()
    deployment.save(update_fields=['started_at'])

    for task in deployment.project.tasks.all():
        task.run(deployment)

    deployment.finished_at = timezone.now()
    deployment.save(update_fields=['finished_at'])

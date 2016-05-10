from celery import shared_task
from django.utils import timezone


@shared_task
def deploy(deployment_id):
    from .models import Deployment
    deployment = Deployment.objects.get(pk=deployment_id)
    deployment.started_at = timezone.now()
    deployment.status = 'pending'
    deployment.save(update_fields=['started_at', 'status'])

    for task in deployment.project.tasks.all():
        task.run(deployment)

    deployment.finished_at = timezone.now()
    deployment.status = deployment.evaluate_status()
    deployment.save(update_fields=['finished_at', 'status'])


@shared_task
def run_deploy_task(task_id):
    from .models import TaskResult
    task = TaskResult.objects.get(pk=task_id)
    return task.run(force=True)

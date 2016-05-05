from celery.app import shared_task

from ..github import update_or_create_webhook


@shared_task
def update_webhook(project_id):
    from .models import Project
    project = Project.objects.get(pk=project_id)
    update_or_create_webhook(project)

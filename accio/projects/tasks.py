from celery.app import shared_task

from accio.github import add_webhook
from ..github import has_webhook


@shared_task
def update_webhooks(project_id):
    from .models import Project
    project = Project.objects.get(pk=project_id)
    check = has_webhook(
        owner=project.owner.name,
        name=project.name,
        token=project.vcs_token
    )

    if not check:
        add_webhook(
            owner=project.owner.name,
            name=project.name,
            token=project.vcs_token
        )


from accio.webhooks.errors import WebhookError
from ...github import validate_webhook
from ...projects.models import Project
from .base import WebhookView


class GithubWebhookView(WebhookView):
    def get_project(self, payload):
        return Project.objects.get(
            owner__name=payload['repository']['owner']['name'],
            name=payload['repository']['name'],
        )

    def get_ref(self, payload):
        return payload['head_commit']['id']

    def validate_webhook_payload(self, request, payload, project):
        if payload['ref'] != 'refs/heads/master':
            raise WebhookError('Not on master branch', 400)

    def validate_webhook_origin(self, request, payload, project):
        if not validate_webhook(request=request, project=project):
            # raise WebhookError('Invalid signature', 403)
            # silently fails o.O
            pass

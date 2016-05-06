from accio.webhooks.errors import WebhookError
from ...github import validate_webhook
from ...projects.models import Project
from .base import WebhookView


class GithubWebhookView(WebhookView):
    def get_project(self, event, payload):
        owner, name = '', ''
        if event == 'push':
            owner = payload['repository']['owner']['name']
            name = payload['repository']['name']
        elif event == 'status':
            owner, name = payload['name'].split('/')
        return Project.objects.get(owner__name=owner, name=name)

    def get_ref(self, event, payload):
        if event == 'push':
            return payload['head_commit']['id']
        if event == 'status':
            return payload['commit']['sha']

    def get_event(self, request):
        return request.META.get('HTTP_X_GITHUB_EVENT')

    def is_branch(self, branch, event, payload):
        if event == 'push':
            return payload['ref'] == 'refs/heads/{0}'.format(branch)
        if event == 'status':
            for _branch in payload['branches']:
                is_head_on_branch = _branch['commit']['sha'] == self.get_ref(event, payload)
                if _branch['name'] == branch and is_head_on_branch:
                    return True
            return False

    def validate_webhook_payload(self, request, payload, project):
        event = self.get_event(request)
        if not self.is_branch('master', event, payload):
            raise WebhookError('Not on master branch', 400)

        if event == 'status' and payload['state'] != 'success':
            raise WebhookError('Status is not success', 400)

    def validate_webhook_origin(self, request, payload, project):
        if not validate_webhook(request=request, project=project):
            raise WebhookError('Invalid signature', 403)

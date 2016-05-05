import json

from django.http import HttpResponse
from django.views.generic import View

from ...projects.models import Project
from ..errors import WebhookError


class WebhookView(View):
    def post(self, request):
        payload = json.loads(str(request.body, encoding='utf-8'))

        try:
            self.handle_webhook(request, payload)
        except WebhookError as error:
            return HttpResponse(error.message, status=error.status_code)
        return HttpResponse('Deploy queued', status=200)

    def handle_webhook(self, request, payload):
        ref = self.get_ref(payload)

        try:
            project = self.get_project(payload)
        except Project.DoesNotExist:
            raise WebhookError('Project does not exist', 404)

        self.validate_webhook_origin(request, payload, project)
        self.validate_webhook_payload(request, payload, project)

        project.deployments.create(project=project, ref=ref).start()

    def get_project(self, payload):
        raise NotImplementedError('get_project is not implemented')

    def get_ref(self, payload):
        raise NotImplementedError('get_ref is not implemented')

    def validate_webhook_origin(self, request, payload, project):
        raise NotImplementedError('validate_webhook_origin is not implemented')

    def validate_webhook_payload(self, request, payload, project):
        raise NotImplementedError('validate_webhook_payload is not implemented')

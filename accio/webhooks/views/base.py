import json
import logging

from django.http import HttpResponse
from django.views.generic import View

from ...projects.models import Project
from ..errors import WebhookError

logger = logging.getLogger(__name__)


class WebhookView(View):
    def post(self, request):
        payload = json.loads(str(request.body, encoding='utf-8'))

        try:
            self.handle_webhook(request, payload)
        except WebhookError as error:
            logger.exception(error, extra={'request': request.__dict__})
            return HttpResponse(error.message, status=error.status_code)
        return HttpResponse('Deploy queued', status=200)

    def handle_webhook(self, request, payload):
        event = self.get_event(request)
        ref = self.get_ref(event, payload)

        try:
            project = self.get_project(event, payload)
        except Project.DoesNotExist:
            raise WebhookError('Project does not exist', 404)

        self.validate_webhook_origin(request, payload, project)
        self.validate_webhook_payload(request, payload, project)

        if event == project.deploy_on:
            project.deployments.create(project=project, ref=ref).start()

    def get_project(self, event, payload):
        raise NotImplementedError('get_project is not implemented')

    def get_ref(self, event, payload):
        raise NotImplementedError('get_ref is not implemented')

    def get_event(self, request):
        raise NotImplementedError('get_event is not implemented')

    def is_branch(self, branch, event, payload):
        raise NotImplementedError('is_branch is not implemented')

    def validate_webhook_origin(self, request, payload, project):
        raise NotImplementedError('validate_webhook_origin is not implemented')

    def validate_webhook_payload(self, request, payload, project):
        raise NotImplementedError('validate_webhook_payload is not implemented')

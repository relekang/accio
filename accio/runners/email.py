from django.conf import settings
from django.core.mail.message import EmailMessage

from .base import Runner


class EmailRunner(Runner):
    def get_commands(self, task):
        return task.config['recipients']

    @staticmethod
    def create_subject(task):
        status = task.deployment.evaluate_status()
        if status == 'success':
            status = 'successful'
        return 'Deployment of {project}@{ref} was {status}'.format(
            project=str(task.deployment.project),
            ref=task.deployment.ref,
            status=status
        )

    @staticmethod
    def create_content(task):
        content = ''
        for task in task.deployment.task_results.all():
            content += task.display_result
        return content

    def run_task(self, task):
        task.result = {}
        for recipient in task.config['recipients']:
            try:
                EmailMessage(
                    subject=self.create_subject(task),
                    to=[recipient],
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    body=self.create_content(task)
                ).send(fail_silently=False)
                task.result[recipient] = {'exit_code': 0}
            except Exception as error:
                task.result[recipient] = {'exit_code': 1, 'error': str(error)}

        task.save()

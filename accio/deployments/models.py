from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models
from django.utils import timezone

from ..runners import get_runner_for_task_type
from ..projects.models import DeploymentTask, DeploymentTaskType
from . import tasks


class Deployment(models.Model):
    project = models.ForeignKey('projects.Project', related_name='deployments')
    ref = models.CharField(max_length=40, help_text='Commit hash or tag name')
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=40, db_index=True)

    def start(self):
        tasks.deploy.delay(self.pk)

    def evaluate_status(self):
        exit_code_sum = 0
        for result in self.task_results.all():
            exit_code_sum += result.exit_code

        if exit_code_sum == 0:
            return 'success'
        return 'failure'


class TaskResult(models.Model):
    task_type = models.CharField(max_length=30, choices=DeploymentTaskType.CHOICES)
    order = models.IntegerField(blank=True)
    config = JSONField(null=True, blank=True)

    deployment = models.ForeignKey(Deployment, related_name='task_results')
    result = JSONField(null=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=40, db_index=True)

    class Meta:
        ordering = ['order']

    @property
    def exit_code(self):
        for key in self.result.keys():
            exit_code = self.result[key]['exit_code']
            if exit_code != 0:
                return exit_code

        return 0

    @property
    def display_result(self):
        output = ''
        line = '----------------------------------'
        if self.config:
            if self.task_type == DeploymentTaskType.SSH:
                for command in self.config['commands']:
                    output += '{0}  ({1}) \n'.format(command, self.result[command]['exit_code'])
                    output += '{0}{0}\n{1}\n\n'.format(line, self.result[command]['stdout'])
            elif self.task_type == DeploymentTaskType.GIT_SSH:
                print('.....')
                exit_code = 0
                for key in self.result.keys():
                    value = self.result[key]
                    exit_code += value['exit_code']
                    if value['stdout']:
                        output += '{0}\n'.format(value['stdout'])
                if exit_code > 0:
                    output += 'It failed'

        return output or self.result

    def run(self):
        self.started_at = timezone.now()
        self.save(update_fields=['started_at'])
        get_runner_for_task_type(self.task_type).run_task(self)
        self.finished_at = timezone.now()
        self.save(update_fields=['finished_at'])

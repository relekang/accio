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


class TaskResult(models.Model):
    task_type = models.CharField(max_length=30, choices=DeploymentTaskType.CHOICES)
    order = models.IntegerField(blank=True)
    config = JSONField(null=True, blank=True)

    deployment = models.ForeignKey(Deployment, related_name='task_results')
    result = JSONField(null=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=40, db_index=True)

    @property
    def display_result(self):
        output = ''
        line = '----------------------------------'
        if self.config:
            for command in self.config['commands']:
                output += '{0}\n'.format(command)
                output += '{1} STDOUT: {1}\n{0}\n\n'.format(self.result[command]['stdout'], line)
                output += '{1} STDERR: {1}\n{0}\n\n'.format(self.result[command]['stderr'], line)

        return output

    def run(self):
        self.started_at = timezone.now()
        self.save(update_fields=['started_at'])
        get_runner_for_task_type(self.task_type).run_tasks(self)
        self.finished_at = timezone.now()
        self.save(update_fields=['finished_at'])

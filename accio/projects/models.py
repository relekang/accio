from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models

from .. import github
from . import tasks
from .managers import ProjectManager


class Project(models.Model):
    owner = models.ForeignKey('organizations.Organization')
    name = models.CharField(max_length=200)
    vcs_url = models.TextField()
    deploy_on = models.CharField(max_length=60, default='status')

    objects = ProjectManager()

    def save(self, *args, **kwargs):
        update_webhook = True
        if 'update_webhook' in kwargs:
            update_webhook = kwargs.pop('update_webhook')
        super().save(*args, **kwargs)
        if update_webhook:
            tasks.update_webhook.delay(self.pk)

    def __str__(self):
        return '{self.owner.name}/{self.name}'.format(self=self)

    @property
    def last_deploy(self):
        return self.deployments.last()

    @property
    def last_deploy_description(self):
        deployment = self.deployments.last()
        if deployment:
            if deployment.finished_at:
                return '{finished_at} - {ref}'.format(**deployment.__dict__)
            return 'Pending - {ref}'.format(**deployment.__dict__)
        return 'Not deployed yet'

    @property
    def vcs_owner(self):
        return self.owner.name

    @property
    def vcs_token(self):
        return self.owner.github_token

    def deploy_latest(self, branch='master'):
        ref = github.get_latest_commit_hash(self, branch)
        self.deployments.create(ref=ref).start()


class DeploymentTaskType(object):
    SSH = 'SSH'
    GIT_SSH = 'GIT_SSH'
    EMAIL_NOTIFICATION = 'EMAIL_NOTIFICATION'
    SLACK_NOTIFICATION = 'SLACK_NOTIFICATION'

    CHOICES = (
        (SSH, 'SSH'),
        (GIT_SSH, 'Git over SSH'),
        (EMAIL_NOTIFICATION, 'Email notification'),
        (SLACK_NOTIFICATION, 'Slack notification'),
    )


class DeploymentTask(models.Model):
    project = models.ForeignKey(Project, related_name='tasks')
    task_type = models.CharField(max_length=30, choices=DeploymentTaskType.CHOICES)
    order = models.IntegerField(blank=True)
    config = JSONField(null=True, blank=True)

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if not self.order:
            self.order = self.project.tasks.count() + 1
        super().save(*args, **kwargs)

    def run(self, deployment):
        deployment.task_results.create(
            task_type=self.task_type,
            order=self.order,
            config=self.config,
        ).run()

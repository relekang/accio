from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models

from .. import github


class Project(models.Model):
    owner = models.ForeignKey('organizations.Organization')
    name = models.CharField(max_length=200)
    vcs_url = models.TextField()

    def __str__(self):
        return self.name

    @property
    def last_deploy(self):
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
        ref = github.get_latest_commit_hash(
            owner=self.vcs_owner,
            name=self.name,
            branch=branch,
            token=self.vcs_token
        )
        self.deployments.create(ref=ref).start()


class DeploymentTaskType(object):
    SSH = 'SSH'
    GIT_SSH = 'GIT_SSH'

    CHOICES = (
        (SSH, 'SSH'),
        (GIT_SSH, 'Git over SSH'),
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

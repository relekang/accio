import requests
from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models


class Project(models.Model):
    owner = models.ForeignKey('organizations.Organization')
    name = models.CharField(max_length=200)
    vcs_url = models.TextField()

    def __str__(self):
        return self.name

    @property
    def last_deploy(self):
        return 'Not deployed yet'

    @property
    def vcs_owner(self):
        return self.owner.name

    def get_latest_commit_hash(self, branch='master'):
        branch_info = requests.get(
            'https://api.github.com/repos/{self.vcs_owner}/{self.name}/branches/{branch}'.format(
                self=self,
                branch=branch
            )
        ).json()
        return branch_info['commit']['sha']

    def deploy_latest(self, branch='master'):
        hash = self.get_latest_commit_hash(branch)
        self.deployments.create(ref=hash).start()


class DeploymentTaskType(object):
    SSH = 'SSH'

    CHOICES = (
        ('SSH', SSH),
    )


class DeploymentTask(models.Model):
    project = models.ForeignKey(Project, related_name='tasks')
    task_type = models.CharField(max_length=30, choices=DeploymentTaskType.CHOICES)
    order = models.IntegerField(blank=True)
    config = JSONField(null=True, blank=True)

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

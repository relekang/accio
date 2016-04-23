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


class DeploymentTasks(models.Model):
    project = models.ForeignKey(Project, related_name='tasks')
    task_type = models.CharField(max_length=30)
    order = models.IntegerField(blank=True)
    config = JSONField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.order:
            self.order = self.project.tasks.count() + 1
        super().save(*args, **kwargs)

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

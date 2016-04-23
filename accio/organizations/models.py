from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField('users.User', blank=True)

    def __str__(self):
        return self.name

from django.db import models
from django.db.models import Q

from ..utils import PermittedQuerySet


class ProjectQuerySet(PermittedQuerySet):
    def permitted_query(self, user):
        return Q(owner__members=user)


class ProjectManager(models.Manager):
    def get_queryset(self):
        return ProjectQuerySet(self.model, using=self._db)

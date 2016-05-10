from django.db import models


class PermittedQuerySet(models.QuerySet):

    allow_anonymous = False

    def permitted_query(self, user):
        raise NotImplementedError

    def permitted(self, user):
        if user.is_anonymous() and not self.allow_anonymous:
            return self.none()
        return self.filter(self.permitted_query(user)).distinct()

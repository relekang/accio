from django.contrib.auth.models import AbstractUser
from django.utils.functional import cached_property
from social.apps.django_app.default.models import UserSocialAuth


class User(AbstractUser):

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_active = False
        super().save(*args, **kwargs)

    @cached_property
    def github_token(self):
        try:
            return self.social_auth.get(provider='github').extra_data['access_token']
        except UserSocialAuth.DoesNotExist:
            return

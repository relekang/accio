from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_staff = True
        super().save(*args, **kwargs)

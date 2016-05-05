from django.views.decorators.csrf import csrf_exempt

from .github import GithubWebhookView

github = csrf_exempt(GithubWebhookView.as_view())

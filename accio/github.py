import hashlib

from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from github3 import login

WEBHOOK_PATH = reverse_lazy('webhooks:github')
WEBHOOK_EVENTS = ['status', 'push', 'deployment']


def create_repository_secret(repository):
    return hashlib.sha224(
        (settings.WEBHOOK_SECRET_KEY + repository.name).encode()
    ).hexdigest()


def login_github(project):
    return login(token=project.vcs_token)


def get_github_repository(project):
    return login_github(project).repository(
        owner=project.owner.name,
        repository=project.name
    )


def get_latest_commit_hash(project, branch):
    repository = get_github_repository(project)
    return repository.branch(branch).commit.sha


def update_or_create_webhook(project):
    repository = get_github_repository(project)
    secret = create_repository_secret(project)
    print(secret)
    for hook in repository.iter_hooks():
        hook_url = hook.config.get('url')
        if hook_url == settings.SERVER_URL + str(WEBHOOK_PATH):
            return update_webhook(hook, secret)

    return add_webhook(repository, secret)


def webhook_settings(secret):
    return dict(
        events=['push'],
        config={
            'url': settings.SERVER_URL + str(WEBHOOK_PATH),
            'content_type': 'json',
            'secret': secret,
        },
        active=True
    )


def add_webhook(repository, secret):
    return repository.create_hook(name='web', **webhook_settings(secret))


def update_webhook(hook, secret):
    return hook.edit(**webhook_settings(secret))
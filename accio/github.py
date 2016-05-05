import hashlib
import hmac
import logging

from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from github3 import login

logger = logging.getLogger(__name__)

WEBHOOK_PATH = reverse_lazy('webhooks:github')
WEBHOOK_EVENTS = ['status', 'push', 'deployment']


def create_project_secret(project):
    return hashlib.sha224(
        (settings.WEBHOOK_SECRET_KEY + project.name).encode()
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
    secret = create_project_secret(project)

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


def validate_webhook(request, project):
    secret = create_project_secret(project)
    name, signature_digest = request.META.get('HTTP_X_HUB_SIGNATURE').split('=')

    hash_builder = hmac.new(secret.encode(), msg=request.body, digestmod=getattr(hashlib, name))
    expected_digest = hash_builder.hexdigest()
    if hmac.compare_digest(expected_digest, signature_digest):
        logger.error('Github webhook validation failed', extra={
            'signature_digest': signature_digest,
            'expected_digest': expected_digest,
            'project': str(project),
            'request': request.__dict__,
        })
        return True
    return False

import json
import os

import pytest
from django.conf import settings
from django.core.urlresolvers import reverse


@pytest.fixture
def relekang_org():
    from .organizations.models import Organization
    return Organization.objects.create(name='relekang')


@pytest.fixture
def accio_project(relekang_org):
    from .projects.models import Project
    return Project.objects.create(
        owner=relekang_org,
        name='accio',
        vcs_url='git@github.com:relekang/accio.git'
    )


@pytest.fixture
def fixture_loader():
    def loader(name, parse_format='json'):
        with open(os.path.join(settings.REPO_DIR, 'fixtures', name)) as f:
            if parse_format == 'json':
                return json.load(f)
            return f.read()

    return loader


@pytest.fixture
def github_webhooks(client, fixture_loader):
    def send_webhook(name, signature):
        return client.post(
            reverse('webhooks:github'),
            json.dumps(fixture_loader('webhooks/github/{0}.json'.format(name))),
            content_type='application/json',
            HTTP_X_GITHUB_EVENT=name,
            HTTP_X_HUB_SIGNATURE='sha1={0}'.format(signature)
        )

    return send_webhook

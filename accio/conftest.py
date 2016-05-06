import hashlib
import hmac
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
    def send_webhook(name, event):
        fixture = json.dumps(fixture_loader('webhooks/github/{0}.json'.format(name)))
        signature = hmac.new(
            b'af8313342e360d966a57c3fb373c74ac9ea616bead86404dfa07d362',
            msg=fixture.encode(),
            digestmod=hashlib.sha1,
        ).hexdigest()

        return client.post(
            reverse('webhooks:github'),
            fixture,
            content_type='application/json',
            HTTP_X_GITHUB_EVENT=event,
            HTTP_X_HUB_SIGNATURE='sha1={0}'.format(signature)
        )

    return send_webhook

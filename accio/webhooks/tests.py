import pytest


@pytest.mark.django_db
def test_github_push_should_deploy(accio_project, github_webhooks):
    response = github_webhooks(name='push', signature='')
    assert response.content.decode() == 'Deploy queued'
    assert response.status_code == 200


@pytest.mark.django_db
def test_github_push_should_deploy_other_branch(accio_project, github_webhooks):
    response = github_webhooks(name='push_other_branch', signature='')
    assert response.content.decode() == 'Not on master branch'
    assert response.status_code == 400

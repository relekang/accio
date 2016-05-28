import pytest


@pytest.fixture
def push_based_project(accio_project):
    accio_project.deploy_on = 'push'
    accio_project.save()
    return accio_project


@pytest.fixture
def status_based_project(accio_project):
    accio_project.deploy_on = 'status'
    accio_project.save()
    return accio_project


@pytest.mark.django_db
def test_github_push_should_deploy(mock_runners, push_based_project, github_webhooks):
    response = github_webhooks(name='push', event='push')
    assert response.content.decode() == 'Deploy queued'
    assert response.status_code == 200


@pytest.mark.django_db
def test_github_push_should_not_deploy_other_branch(push_based_project, github_webhooks):
    response = github_webhooks(name='push_other_branch', event='push')
    assert response.content.decode() == 'Not on master branch'
    assert response.status_code == 400


@pytest.mark.django_db
def test_github_status_success_should_deploy(mock_runners, status_based_project, github_webhooks):
    response = github_webhooks(name='status_success', event='status')
    assert response.content.decode() == 'Deploy queued'
    assert response.status_code == 200


@pytest.mark.django_db
def test_github_status_failure_should_not_deploy(status_based_project, github_webhooks):
    response = github_webhooks(name='status_failure', event='status')
    assert response.content.decode() == 'Status is not success'
    assert response.status_code == 400


@pytest.mark.django_db
def test_github_status_not_master_should_not_deploy(status_based_project, github_webhooks):
    response = github_webhooks(name='status_not_master', event='status')
    assert response.content.decode() == 'Not on master branch'
    assert response.status_code == 400

import pytest


@pytest.mark.django_db
def test_deployment_task_run_should_combine_configs(mock_runners, accio_project):
    deployment = accio_project.deployments.create(ref='master')
    deployment.start()
    assert deployment.task_results.last().config == {'commands': ['ls'], 'hostname': 'host'}


@pytest.mark.django_db
def test_deployment_task_run_should_support_empty_project_config(mock_runners, accio_project):
    accio_project.config = None
    accio_project.save()
    deployment = accio_project.deployments.create(ref='master')
    deployment.start()
    assert deployment.task_results.last().config == {'commands': ['ls']}


@pytest.mark.django_db
def test_deployment_task_run_should_support_empty_task_configs(mock_runners, accio_project):
    accio_project.tasks.update(config=None)
    deployment = accio_project.deployments.create(ref='master')
    deployment.start()
    assert deployment.task_results.last().config == {'hostname': 'host'}

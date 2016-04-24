from accio.runners.git_ssh import GitSshRunner
from accio.runners.ssh import SshRunner
from ..projects.models import DeploymentTaskType

ssh_runner = SshRunner()
git_ssh_runner = GitSshRunner()

runner_type_map = {
    DeploymentTaskType.SSH: ssh_runner,
    DeploymentTaskType.GIT_SSH: git_ssh_runner
}


def get_runner_for_task_type(task_type):
    return runner_type_map.get(task_type, None)

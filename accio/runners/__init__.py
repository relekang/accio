from accio.runners.ssh import SshRunner
from ..projects.models import DeploymentTaskType

ssh_runner = SshRunner()

runner_type_map = {
    DeploymentTaskType.SSH: ssh_runner
}


def get_runner_for_task_type(task_type):
    return runner_type_map.get(task_type, None)

from ..runners.email import EmailRunner
from ..runners.git_ssh import GitSshRunner
from ..runners.ssh import SshRunner
from ..projects.models import DeploymentTaskType

ssh_runner = SshRunner()
git_ssh_runner = GitSshRunner()
email_notification_runner = EmailRunner()

runner_type_map = {
    DeploymentTaskType.SSH: ssh_runner,
    DeploymentTaskType.GIT_SSH: git_ssh_runner,
    DeploymentTaskType.EMAIL_NOTIFICATION: email_notification_runner
}


def get_runner_for_task_type(task_type):
    return runner_type_map.get(task_type, None)

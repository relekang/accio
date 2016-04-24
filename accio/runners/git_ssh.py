from django.conf import settings
from paramiko import SSHClient, AutoAddPolicy

from .base import Runner


class GitSshRunner(Runner):
    def run_tasks(self, task):
        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(
            hostname=task.config['hostname'],
            username=task.config['username'],
            key_filename=settings.PRIVATE_KEY_FILENAME
        )

        task.result = {}
        commands = [
            'cd {path} && git fetch'.format(**task.config),
            'cd {path} && git reset --hard {ref}'.format(ref=task.deployment.ref, **task.config)
        ]

        for command in commands:
            task.result[command] = {}
            stdin, stdout, stderr = client.exec_command(command)
            task.result[command]['stdout'] = stdout.read().decode()
            task.result[command]['stderr'] = stderr.read().decode()
            task.save()

from django.conf import settings
from paramiko import AutoAddPolicy, SSHClient

from .base import Runner


class SshRunner(Runner):
    @staticmethod
    def set_up_client(task):
        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(
            hostname=task.config['hostname'],
            username=task.config['username'],
            key_filename=settings.PRIVATE_KEY_FILENAME,
        )

        return client

    @staticmethod
    def run_command(command, client):
        result = {}
        channel = client.get_transport().open_session()
        channel.set_combine_stderr(True)

        channel.exec_command(command)
        result['stdout'] = channel.recv(1024 * 1024 * 1024).decode()
        result['exit_code'] = channel.recv_exit_status()
        return result

    def run_task(self, task):
        client = self.set_up_client(task)
        task.result = {}

        for command in self.get_commands(task):
            task.result[command] = self.run_command(command, client)
            task.save()

        client.close()

    def get_commands(self, task):
        return task.config['commands']

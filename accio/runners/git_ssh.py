from .ssh import SshRunner


class GitSshRunner(SshRunner):
    def get_commands(self, task):
        return [
            'cd {path} && git fetch'.format(**task.config),
            'cd {path} && git reset --hard {ref}'.format(ref=task.deployment.ref, **task.config)
        ]

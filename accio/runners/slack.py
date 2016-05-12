import json

import requests

from .base import Runner


class SlackNotificationRunner(Runner):
    def get_commands(self, task):
        return task.config['channels']

    @staticmethod
    def get_text(task):
        return 'Deployment of {owner}/{name} was a {status}'.format(
            owner=task.deployment.project.owner.name,
            name=task.deployment.project.name,
            status=task.deployment.evaluate_status()
        )

    def send(self, task, channel):
        icon = 'rocket'
        if 'slack_icon' in task.config:
            icon = task.config['slack_icon']

        requests.post(task.config['slack_url'], json.dumps({
            'icon_emoji': icon,
            'channel': channel,
            'text': self.get_text(task),
            'username': 'accio',
        }))

    def run_task(self, task):
        task.result = {}
        for channel in task.config['channels']:
            try:
                self.send(task, channel)
                task.result[channel] = {'exit_code': 0}
            except Exception as error:
                task.result[channel] = {'exit_code': 1, 'error': error}
            task.save()

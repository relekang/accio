import json

import requests
from django.conf import settings
from django.core.urlresolvers import reverse


class ApiRequestError(Exception):
    pass


def api_request(url, token, data=None, page=None):
    url = "https://api.github.com%s?access_token=%s" % (url, token)
    if page:
        url += '&page=%s' % page
    if data is None:
        response = requests.get(url)
    else:
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/vnd.github.she-hulk-preview+json'
        }
        response = requests.post(url, data=json.dumps(data), headers=headers)

    if settings.DEBUG:
        print((response.headers.get('X-RateLimit-Remaining')))

    if response.status_code < 400:
        raise ApiRequestError(response)

    return response


def get_latest_commit_hash(**kwargs):
    branch_info = api_request(
        '/repos/{owner}/{name}/branches/{branch}'.format(**kwargs),
        kwargs['token']
    ).json()
    return branch_info['commit']['sha']


def has_webhook(**kwargs):
    hooks = api_request(
        '/repos/{owner}/{name}/hooks'.format(**kwargs),
        kwargs['token']
    ).json()
    for hook in hooks:
        if hook['config']['url'] == settings.SERVER_URL + reverse('webhooks:github'):
            return True
    return False


def add_webhook(**kwargs):
    return api_request(
        '/repos/{owner}/{name}/hooks'.format(**kwargs),
        kwargs['token'],
        data={
            'name': 'web',
            'events': [],
            'active': True,
            'config': {
                'url': settings.SERVER_URL + reverse('webhooks:github'),
                'content_type': 'json'
            }
        }
    ).json()

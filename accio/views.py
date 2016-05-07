import json

from django.conf import settings
from django.http.response import HttpResponse
from django.shortcuts import render
from djangorestframework_camel_case.render import CamelCaseJSONRenderer

from accio.projects.models import Project
from accio.projects.serializers import ProjectSerializer
from accio.users.serializers import UserSerializer


def index(request):
    user_data = UserSerializer(request.user).data
    if request.user.is_authenticated():
        projects = Project.objects.filter(owner__members=request.user)
        projects_data = [ProjectSerializer(project).data for project in projects]
    else:
        projects_data = []
    return render(request, 'index.html', {
        'user_info': json.dumps(CamelCaseJSONRenderer().render(user_data).decode()),
        'projects': json.dumps(CamelCaseJSONRenderer().render(projects_data).decode()),
        'debug': settings.DEBUG,
    })


def public_key(request):
    with open(settings.PUBLIC_KEY_FILENAME, 'r') as f:
        return HttpResponse(f.read(), content_type='text/plain')

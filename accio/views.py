from django.conf import settings
from django.http.response import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def public_key(request):
    with open(settings.PUBLIC_KEY_FILENAME, 'r') as f:
        return HttpResponse(f.read(), content_type='text/plain')

from django.http.response import HttpResponse


def webhook(request):
    return HttpResponse('Webhooks not implemented yet', status=501)

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def webhook(request):
    return HttpResponse('Webhooks not implemented yet', status=501)

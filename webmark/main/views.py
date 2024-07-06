from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .APIhandler import API


def index(request: HttpRequest, data = {}):
    if request.method == "GET":
        return render(request, 'main/index.html', data)


@csrf_exempt
def api_handler(request: HttpRequest):
    api = API()
    data = api.request_update(request.POST)
    return JsonResponse(data=data, status=200)
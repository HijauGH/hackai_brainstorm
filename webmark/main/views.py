from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .APIhandler import API

@csrf_exempt
def index(request: HttpRequest):
    api = API()
    if request.method == "POST":
        data = api.get_point_request(request.POST)
        return JsonResponse(data=data, status=200)

    else:
        return JsonResponse(data=api.get_all_point_request(), status=200)


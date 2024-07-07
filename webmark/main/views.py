import json

from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .APIhandler import API

@csrf_exempt
def index(request):
    api = API()
    print(request)
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        data = api.get_point_request(body_data)
        return JsonResponse(data=data, status=200)
    else:
        return JsonResponse(data=api.get_all_point_request(), status=200)


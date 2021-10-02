import requests
import os

from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse

from . import request_nasa


API_URL = os.getenv('API_URL')


@csrf_exempt
def main_view(request):
    response = {
        "status": "up and running"
    }

    return JsonResponse(response)


def request_info_nasa(request):
    json_response = request_nasa.testing(request)

    return JsonResponse(json_response)


def receive_info_from_front(request):
    endpoint = 'api/temporal/monthly/point'
    body = request.GET

    required = {
        'start': body.get('start'),
        'end': body.get('end'),
        'latitude': body.get('latitude'),
        'longitude': body.get('longitude'),
        'community': 'sb',
        'parameters': 'ALLSKY_SFC_SW_DWN',
    }

    r = requests.get(
        API_URL + endpoint,
        params=required
    )

    api_response = r.json()

    return JsonResponse(api_response)
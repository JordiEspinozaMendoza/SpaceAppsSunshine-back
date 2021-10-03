from django.http.response import JsonResponse

from . import request_nasa


def main_view(request):
    response = {
        "Status": "up and running"
    }

    return JsonResponse(response)


def request_info_nasa(request):
    json_response = request_nasa.testing(request)

    return JsonResponse(json_response)


def receive_info_from_front(request):
    endpoint = 'api/temporal/monthly/point'
    body = request.GET

    received_data = {
        'start': body.get('start'),
        'end': body.get('end'),
        'latitude': body.get('latitude'),
        'longitude': body.get('longitude'),
        'community': 'sb',
        'format': 'json',
    }

    NasaInfo = request_nasa.NasaInfo(received_data)
    final_data = NasaInfo.return_data_from_nasa()

    return JsonResponse(final_data)
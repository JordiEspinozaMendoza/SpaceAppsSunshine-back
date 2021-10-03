from django.http.response import JsonResponse

from . import request_nasa


def main_view(request):
    response = {
        "Status": "up and running"
    }

    return JsonResponse(response)


def request_info_nasa(request):
    json_response = request_nasa.windrose(request)

    return JsonResponse(json_response)


def receive_info_from_front(request):
    body = request.GET

    received_data = {
        'start': body.get('start'),
        'end': body.get('end'),
        'latitude': body.get('latitude'),
        'longitude': body.get('longitude'),
        'resolution': body.get('resolution'),
        'community': 'sb',
        'format': 'json',
    }

    resolution = received_data.get('resolution')
    if resolution == 'yearly':
        resolution = 'monthly'
    elif resolution == 'weekly':
        resolution = 'daily'

    NasaInfo = request_nasa.NasaInfo(
        received_data, resolution,
        #['Solar Fluxes and Related', 'Temperature/Thermal IR Flux', 'DOE/ASHRAE Climate Building', 'Humidity/Precipitation', 'Wind/Pressure']
        request_nasa.Parameters(resolution).__dict__
    )

    if NasaInfo.is_fail():
        return JsonResponse({'message': 'error'}, status=500)

    data = NasaInfo.return_data_from_nasa()

    return JsonResponse({'array': data})

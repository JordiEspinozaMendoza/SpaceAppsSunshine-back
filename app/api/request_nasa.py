import requests
import os


API_URL = os.getenv('API_URL')


def testing(request):
    endpoint = 'api/temporal/monthly/point'
    body = request.GET

    r = requests.get(
        API_URL + endpoint,
        params=body
    )

    api_response = r.json()

    return api_response


def testing2(request):
    endpoint = 'api/temporal/monthly/point'
    body = request.GET

    r = requests.get(
        API_URL + endpoint,
        params=body
    )

    api_response = r.json()

    return api_response
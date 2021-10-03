import requests
import os


API_URL = os.getenv('API_URL')


class NasaInfo:
    def __init__(self, received_data):
        self.received_data = received_data
        self.graph_types = ['ALLSKY_SFC_SW_DWN', 'ALLSKY_SFC_SW_DWN']
        #formated_data = format_data(received_data)


    def request_data(self, data_type):
        endpoint = 'api/temporal/monthly/point'
        body = self.received_data
        body['parameters'] = data_type

        r = requests.get(
            API_URL + endpoint,
            params=body
        )

        api_response = r.json()

        return api_response


    def return_data_from_nasa(self):
        final_data = []

        for graph_type in self.graph_types:
            raw_data = self.request_data(graph_type)
            # formatear raw_data
            # una vez formateado -> lo añado a un array
            final_data.append(raw_data)
        
        return final_data
import requests
import os


API_URL = os.getenv('API_URL')


class NasaInfo:
    def __init__(self, received_data):
        self.received_data = received_data
        self.graph_types = ['ALLSKY_SFC_SW_DWN', 'ALLSKY_SFC_SW_DWN']


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
            formatted_data = {
                graph_type: FormatData(raw_data,
                self.received_data.get('resolution'),
            ).__dict__
            }
            final_data.append(formatted_data)
        
        return final_data


class FormatData:
    def __init__(self, graph_raw, resolution):
        self.values = []
        self.title = ''
        self.values_units = '',
        self.resolution = resolution
        self.format_graph(graph_raw)
    
    def format_graph(self, graph_raw):
        parameter = graph_raw.get('properties').get('parameter')
        self.title = list(parameter.keys())[0]
        items = list(parameter.get(self.title).values())
        self.values_units = graph_raw.get('parameters').get(self.title).get('units')

        if self.resolution == 'monthly' or self.resolution == 'yearly':
            anual_avg = []
            avg_items = len(items) // 13

            for i in range(avg_items, 0, -1):
                anual_avg.append(items.pop(i * 13 - 1))
            anual_avg.reverse()
            
            if self.resolution == 'monthly':
                self.values = items
            else:
                self.values = anual_avg

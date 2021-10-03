import requests
import os
import sys

from datetime import datetime, timedelta


API_URL = os.getenv('API_URL')


class NasaInfo:
    def __init__(self, received_data, api_resolution):
        self.received_data = received_data
        self.api_resolution = api_resolution
        self.graph_types = ['ALLSKY_SFC_SW_DWN', 'ALLSKY_SFC_SW_DWN']

    def request_data(self, data_type):
        endpoint = f'api/temporal/{self.api_resolution}/point'
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

    def is_fail(self):
        try:
            start_date = self.received_data.get('start')
            end_date = self.received_data.get('end')
            now = datetime.now()

            if self.api_resolution == 'monthly':
                now_year = now.year

                if int(start_date) < 1981 \
                        or int(start_date) >= now_year:
                    return True

                if int(end_date) < int(start_date) \
                        or int(end_date) >= now_year:
                    return True
            else:
                start_date_obj = datetime(
                    year=int(start_date[:4]),
                    month=int(start_date[4:6]),
                    day=int(start_date[6:])
                )

                end_date_obj = datetime(
                    year=int(end_date[:4]),
                    month=int(end_date[4:6]),
                    day=int(end_date[6:])
                )

                if start_date_obj.year < 1981 \
                        or start_date_obj >= now:
                    return True

                if end_date_obj < start_date_obj \
                        or end_date_obj >= now:
                    return True

        except Exception:
            err = sys.exc_info()
            print('resolve_req', err)
            exception_traceback = err[2]
            print('line_number', exception_traceback.tb_lineno)
            return True

        return False


class FormatData:
    def __init__(self, graph_raw, resolution):
        self.values = []
        self.title = ''
        self.values_units = '',
        self.resolution = resolution
        self.format_graph(graph_raw)

    def format_graph(self, graph_raw):
        parameter = graph_raw.get('properties').get('parameter')
        key = list(parameter.keys())[0]
        items = list(parameter.get(key).values())
        self.values_units = graph_raw.get('parameters').get(key).get('units')
        self.title = graph_raw.get('parameters').get(key).get('longname')

        self.values = items

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

import requests
import os
import sys

from datetime import datetime, timedelta

from functools import reduce

API_URL = os.getenv('API_URL')


class NasaInfo:
    def __init__(self, received_data, api_resolution, parameters):
        self.received_data = received_data
        self.api_resolution = api_resolution
        self.graph_types = parameters['values']
        self.delta = None

    def request_data(self, data_type):
        endpoint = f'/api/temporal/{self.api_resolution}/point'
        body = self.received_data
        body['parameters'] = ','.join(data_type)

        r = requests.get(
            API_URL + endpoint,
            params=body
        )
        api_response = r.json()

        return api_response

    def return_data_from_nasa(self):
        final_data = []

        raw_data = self.request_data(self.graph_types)

        for graph_type in self.graph_types:
            final_data.append({
                graph_type: FormatData(raw_data, self.received_data.get('resolution'),
                                       self.delta, graph_type).__dict__
            })

        return final_data

    def is_fail(self):
        try:
            start_date = self.received_data.get('start')
            end_date = self.received_data.get('end')
            now = datetime.now()

            if self.api_resolution == 'monthly':

                self.received_data['start'] = datetime.strptime(
                    start_date[:4], '%Y').year
                start_date = self.received_data['start']

                self.received_data['end'] = datetime.strptime(
                    end_date[:4], '%Y').year
                end_date = self.received_data['end']

                now_year = now.year

                if int(start_date) < 1981 \
                        or int(start_date) >= now_year:
                    return True

                if int(end_date) < int(start_date) \
                        or int(end_date) >= now_year:
                    return True
            else:
                start_date_obj = datetime.strptime(start_date, '%Y%m%d')
                end_date_obj = datetime.strptime(end_date, '%Y%m%d')

                if start_date_obj.year < 1981 \
                        or start_date_obj >= now:
                    return True

                if end_date_obj < start_date_obj \
                        or end_date_obj >= now:
                    return True

            if self.received_data.get('resolution') == 'weekly':
                start_date_obj = datetime.strptime(start_date, '%Y%m%d')

                start_start = start_date_obj - \
                    timedelta(days=start_date_obj.weekday())
                end_start = start_start + timedelta(days=6)

                if start_date_obj.year != start_start.year:
                    start_start = datetime(
                        year=start_date_obj.year, month=1, day=1)
                real_dt_start = end_start - start_start

                end_date_obj = datetime.strptime(end_date, '%Y%m%d')

                start_end = end_date_obj - \
                    timedelta(days=end_date_obj.weekday())
                end_end = start_end + timedelta(days=6)

                if end_date_obj.year != end_end.year:
                    end_end = datetime(
                        year=end_date_obj.year, month=12, day=31)

                self.delta = real_dt_start.days

                self.received_data['start'] = start_start.strftime('%Y%m%d')
                self.received_data['end'] = end_end.strftime('%Y%m%d')

        except Exception:
            err = sys.exc_info()
            print('resolve_req', err)
            exception_traceback = err[2]
            print('line_number', exception_traceback.tb_lineno)
            return True

        return False


class FormatData:
    def __init__(self, graph_raw, resolution, delta, graph_type):
        self.values = []
        self.title = ''
        self.values_units = '',
        self.resolution = resolution
        self.format_graph(graph_raw, delta, graph_type)

    def format_graph(self, graph_raw, delta, key):
        parameter = graph_raw.get('properties').get('parameter')
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

        elif self.resolution == 'weekly':
            weekly_avg = [reduce(lambda a, b: a + b,
                                 items[0:delta])/delta]

            i = delta

            while i < len(items):
                dt = i+7
                result = list(filter(lambda x: x >= 0, items[i:dt]))
                weekly_avg.append(
                    reduce(lambda a, b: a + b, result)/len(result))
                i = dt

            self.values = weekly_avg


class Parameters():
    def __init__(self, type, resolution):
        self.values = self.get_type(type, resolution)

    def get_type(self, type, resolution):
        endpoint = "/api/system/manager/parameters"
        body = {
            'community': 'sb',
            'temporal': resolution,
        }

        r = requests.get(
            API_URL + endpoint,
            params=body
        )

        api_response = r.json()

        resolve = []
        for parameter in api_response:
            if '_SD' not in parameter and '_MAX' not in parameter and '_MIN' not in parameter and '_HR' not in parameter and '_0' not in parameter and '_1' not in parameter and '_2' not in parameter and api_response.get(parameter).get('type') == type and ('Irradiance' in api_response.get(parameter).get('name')):
                resolve.append(parameter)

        return resolve

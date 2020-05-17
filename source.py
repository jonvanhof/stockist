from interfaces import http
from parse.stk_csv import csv_parse


class Source:
    def __init__(self, name, source_type, base_url_path):
        self.nm = name
        self.type = source_type
        if source_type == "html" or source_type == "json":
            self.http = http(base_url_path)
        elif source_type == "csv":
            self.path = base_url_path
        else:
            raise ValueError('Invalid or unsupported source type')

    def request(self, ext_url):
        return self.http.request(ext_url)

    def read(self, file_name):
        return csv_parse(self.path, file_name)

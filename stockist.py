from source import Source
from object import Object
from stock_request import StockRequest
from endpoint import Endpoint
import sqlite3


class Stockist:
    def __init__(self, name):
        self.sources = []
        self.objects = []
        self.stock_requests = []
        self.endpoints = []

        self.db = sqlite3.connect(name + ".db", check_same_thread=False)

    def add_source(self, name, src_type, url):
        self.sources.append(Source(name, src_type, url))

    def add_object(self, name, fields, shelf_life):
        self.objects.append(Object(name, fields, shelf_life, self.db))

    def add_stock_request(self, src, obj, url_path, trans_func):
        self.stock_requests.append(StockRequest(src, obj, url_path, trans_func))

    def add_endpoint(self, path, obj, params=None, output_func=None):
        # Create base endpoint
        self.endpoints.append(Endpoint(path, obj, out_func=output_func))
        # Create endpoints for any passed parameters
        if params:
            for i in params:
                self.endpoints.append(Endpoint(path, obj, i, output_func))

    def create_endpoints(self, app):
        for i in self.endpoints:
            if i.params:
                url = i.path + "/<" + i.params + ">"
                nm = i.obj.nm + "_" + i.params
                app.add_url_rule(url, nm, view_func=i.out)
            else:
                app.add_url_rule(i.path, i.obj.nm, view_func=i.out)


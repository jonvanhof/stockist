from parse.stk_json import json_parse
from parse.stk_html import html_parse


class StockRequest:
    def __init__(self, src, obj, url_path, transform_function):
        self.source = src
        self.object = obj
        self.path = url_path

        if callable(transform_function):
            self.trans = transform_function
        else:
            raise ValueError('Transformation must be in the form of a ' +
                             'function.')

    def stock(self, params=None):
        param_string = ""
        if params:
            for i, j in params.items():
                param_string += "&" + i + "='" + j + "'"
        raw_data = self.source.request(self.path + param_string)
        parse_data = []
        if self.source.type == "json":
            parse_data = json_parse(raw_data)
        elif self.source.type == "html":
            parse_data = html_parse(raw_data)

        ret_data = self.trans(parse_data)

        if len(ret_data[0]) != len(list(self.object.fields)):
            raise ValueError('Source fields not present in Object definition.')
        else:
            self.object.put(ret_data)

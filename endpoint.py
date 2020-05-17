from parse.stk_json import jsonify


class Endpoint:
    def __init__(self, path, obj, params=None, out_func=None):
        self.path = '/' + path
        self.obj = obj
        self.out = out_func
        self.params = params

        if not self.out:
            self.out = self.get_out

    def get_out(self, **kwargs):
        return jsonify(self.obj.get(kwargs))

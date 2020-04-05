import os
import csv as df_csv
import codecs

class csv():
    def __init__(self, path, filename):
        self.path = path
        self.f = filename

    def imp_csv(self, dict_key):
        ret_dict = {}
        with codecs.open(self.path + self.f, 'rb', encoding='utf-8-sig') as z_in:
            innie = df_csv.DictReader(z_in, delimiter=',', quotechar='"')
            for i in innie:
                ret_dict[i[dict_key]] = i
        
        return ret_dict

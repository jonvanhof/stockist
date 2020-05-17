import os
import csv
import codecs


def csv_parse(path, file_name):
    ret_list = []
    with codecs.open(path + file_name, 'rb', encoding='utf-8-sig') as z_in:
        innie = csv.DictReader(z_in, delimiter=',', quotechar='"')
        for i in innie:
            ret_list.append(i)
        
    return ret_list

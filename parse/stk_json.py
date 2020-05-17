from json import loads, dumps
from re import split, match
from datetime import datetime as dt


def json_parse(input_string, croptop=None, parse_url=None):
    ret_dict = loads(input_string)

    if croptop is not None:
        ret_dict = ret_dict[croptop]

    if parse_url is not None:
        subs = split("[/]", parse_url)
        for i in subs:
            obj = match("(\w+)", i).group(1)
            # if subs.index(i) != len(subs)-1:
            if obj in ret_dict:
               if len(subs) - 1 == subs.index(i):
                   ret_dict = ret_dict[obj]
                   if 'count' in ret_dict:
                       del(ret_dict['count'])
               else:
                   ret_dict = rootdown(ret_dict, obj)
            #    ret_dict = ret_dict[obj]
            #    del(ret_dict['count'])

    return ret_dict


def rootdown(input_dict, obj):
    if 'count' in input_dict[obj]:
        if input_dict[obj]['count'] == 1:
            ret_dict = input_dict[obj]['0'][obj[:-1]]
        else:
            ret_dict = input_dict[obj]
            del(ret_dict['count'])
    else:
        ret_dict = input_dict[obj]

    if len(ret_dict) == 1:
        return ret_dict[0]
    elif len(ret_dict) == 2:
        return ret_dict[1]
    else:
        return ret_dict


def to_dt_string(in_dt):
    return in_dt.strftime('%m-%d-%Y')


def jsonify(in_data):
    if type(in_data) == list:
        for i in in_data:
            if type(i) == dict:
                for j, k in i.items():
                    if type(k) is dt:
                        i[j] = to_dt_string(k)
    return dumps(in_data)

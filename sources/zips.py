from parse.stk_csv import csv_parse
from datetime import datetime as dt

class zips:
    def __init__(self, path, year=None):
        self.path = path
        if year is None:
            self.yr = str(dt.today().year)
        else:
            self.yr = year

    def read(self):
        ret_list = []
        raw_hit = csv_parse(self.path, 'zips_' + self.yr + '_hitters.csv', 
          'Name')
        raw_pitch = csv_parse(self.path, 'zips_' + self.yr + '_pitchers.csv', 
          'Name')

        for i in raw_hit:
            i['name'] = i.pop('Name')
            i['team'] = i.pop('Team')
            i['DB'] = i.pop('2B')
            i['TR'] = i.pop('3B')
            if i['playerid'][0:2] == 'sa':
                i['playerid'] = i['playerid'][2:]
            ret_list.append(i)
        
        for i in raw_pitch:
            i['name'] = i.pop('Name')
            i['team'] = i.pop('Team')
            i['BB9'] = i.pop('BB/9')
            i['K9'] = i.pop('K/9')
            if i['playerid'][0:2] == 'sa':
                i['playerid'] = i['playerid'][2:]
            for j in ret_list:
                if i['playerid'] == j['playerid']:
                    i['playerid'] = '2' + i['playerid']
            ret_list.append(i)

        return ret_list
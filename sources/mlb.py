from interfaces import http
from parse.stk_json import json_parse
from datetime import datetime as dt

class mlb:
    def __init__(self):
        self.http = \
          http("http://lookup-service-prod.mlb.com/json/named.")

    def request(self, ext_url):
        res = self.http.request(ext_url)
        
        return json_parse(res)

    def get_player(self, name):
        raw_data = self.request("search_player_all.bam?sport_code='mlb'" +
          "&name_part='" + name + "'")
        if 'row' in raw_data['search_player_all']['queryResults']:
            raw_plyrs = raw_data['search_player_all']['queryResults']['row']
        else: 
            raw_plyrs = []

        ret_plyrs=[]
        if isinstance(raw_plyrs, list):
            for i in raw_plyrs:
                ret_plyrs.append(self.mk_plyr(i))
        else:
            ret_plyrs.append(self.mk_plyr(raw_plyrs))

        if len(ret_plyrs) == 0:
            raw_data = self.request("milb_player_search.bam?name_part='" +
              name + "'")
            if 'row' in raw_data['milb_player_search']['queryResults']:
                raw_plyrs = raw_data['milb_player_search']['queryResults']['row']
            if isinstance(raw_plyrs, list):
                for i in raw_plyrs:
                    ret_plyrs.append(self.mk_plyr_milb(i))
            else:
                ret_plyrs.append(self.mk_plyr_milb(raw_plyrs))
        else:
            return ret_plyrs

        if len(ret_plyrs) == 0:
            p_n = name.split()
            p_n[0] = p_n[0].replace(".", "")
            raw_data = self.request("search_player_all.bam?sport_code='mlb'" +
              "&name_part='" + p_n[0] + "% " + p_n[1] + "%'")
            if 'row' in raw_data['search_player_all']['queryResults']:
                raw_plyrs = raw_data['search_player_all']['queryResults']['row']
            if isinstance(raw_plyrs, list):
                for i in raw_plyrs:
                    ret_plyrs.append(self.mk_plyr(i))
            else:
                ret_plyrs.append(self.mk_plyr(raw_plyrs))
        else:
            return ret_plyrs

        if len(ret_plyrs) == 0:
            p_n = name.split()
            raw_data = self.request("milb_player_search.bam?name_part='" +
              p_n[0][0:2] + "% " + p_n[1] + "%'&active_sw='Y'")
            if 'row' in raw_data['milb_player_search']['queryResults']:
                raw_plyrs = raw_data['milb_player_search']['queryResults']['row']
            if isinstance(raw_plyrs, list):
                for i in raw_plyrs:
                    ret_plyrs.append(self.mk_plyr_milb(i))
            else:
                ret_plyrs.append(self.mk_plyr_milb(raw_plyrs))
        else:
            return ret_plyrs

        return ret_plyrs

    def mk_plyr(self, plyr):
        return {'name' : plyr['name_display_first_last'],
                'id' : plyr['player_id'],
                'team' : plyr['team_full'],
                'pos' : plyr['position'],
                'level' : plyr['sport_code'],
                'birth_dt' : dt.strptime(plyr['birth_date'][0:10], '%Y-%m-%d')}

    def mk_plyr_milb(self, plyr):
        ret_plyr = {'name' : plyr['name_first_last'],
                    'id' : plyr['player_id'],
                    'team' : plyr['team_name'],
                    'level' : plyr['level'],
                    'birth_dt' : dt.strptime(plyr['player_birth_date'][0:10], 
                      '%Y-%m-%d')}
        if plyr['primary_position'] == "1":
            ret_plyr['pos'] = "P"
        else:
            ret_plyr['pos'] = plyr['primary_position']

        return ret_plyr
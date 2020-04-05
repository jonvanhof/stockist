from interfaces import http
from parse.stk_json import json_parse
from datetime import datetime as dt

class milb:
    def __init__(self):
        self.http = http("http://www.milb.com/lookup/json/named.")

    def request(self, ext_url):
        res = self.http.request(ext_url)
        
        return json_parse(res)

    def get_system(self, season=None):
        if season is None:
            season = str(dt.today().year)

        raw_data = self.request("milb_standings_display_flip.bam?season=" +
          season)
        raw_system = raw_data['milb_standings_display_flip']['org_history']\
          ['queryResults']['row']

        ret_system=[]
        for i in raw_system:
            ret_system.append({'name' : i['name_full'],
                'id' : i['organization_id'],
                'abbrev' : i['name_abbrev'],
                'org_code' : i['org_code'],
                'parent_org' : i['parent_org'],
                'type' : i['org_type']})

        return ret_system

    def get_teams(self, season=None, league_id=None):
        if season is None:
            season = str(dt.today().year)

        raw_data = self.request("milb_standings_display_flip.bam?season=" + 
          season)
        raw_teams = raw_data['milb_standings_display_flip']['team_all_season']\
          ['queryResults']['row']

        ret_teams=[]
        for i in raw_teams:
            if 'mlb_org_id' in i and i['mlb_org_id'] != '':
              if int(i['mlb_org_id']) >= 100:
            #if i['sport_code'] == 'mlb' and i['city'] != '': #and \
                  #i['all_star_sw'] == 'N' or i['mlb_org_id'] != '':
                ret_teams.append({'code' : i['sport_code'],
                  'id' : i['team_id'],
                  'abbrev' : i['name_abbrev'],
                  'city' : i['city'],
                  'name' : i['name'],
                  'full_name' : i['name_display_long'],
                  'league_id' : i['league_id'],
                  'state' : i['state'],
                  'venue_id' : i['venue_id'],
                  'venue_name' : i['venue_name'],
                  'org' : i['mlb_org'],
                  'org_id' : i['mlb_org_id']})

        return ret_teams

    def get_team_schedule(self, team_id, season=None):
        if season is None:
            season = str(dt.today().year)
        #elif:
        #    seas_url = "&start_date=%27" + season + 
        #      "%2F01%2F01%27&end_date=%27" + season + "%2F12%2F31%27"


        raw_schedule = self.request("schedule_team_complete.bam?season=" + 
          season + "&team_id=" + team_id)
        schedule = raw_schedule['schedule_team_complete']['queryResults']['row']

        ret_schedule = []
        for i in schedule:
            if i['game_type'] == 'R':
              ret_schedule.append({
                "team_id" : i['team_id'],
                "team_lg" : i['league_id'],
                "team_tz" : i['team_time_zone'],
                "opp_id" : i['opponent_id'],
                "opp_lg" : i['opponent_league_id'],
                "opp_tz" : i['opponent_time_zone'],
                "venue" : i['venue_name'],
                "loc" : i['venue_city'] + ', ' + i['venue_twc_loc'][2:4],
                "loc_tz" : i['time_zone_local'],
                "home_away" : i['home_away_sw'],
                "double_header" : i['double_header_sw'],
                "game_num" : i['game_nbr'],
                "gametime" : dt.strptime(i['game_time_et'],
                    '%Y-%m-%dT%H:%M:%S')})

        return ret_schedule

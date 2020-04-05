from interfaces import oauth2
from parse.stk_json import json_parse
from datetime import datetime as dt

class yfs:
    '''
    def __init__(self, consumer_key, consumer_secret, token=None, \
      token_secret=None, handle=None):
        
        #OAuth 1.0 Configuration
        oauth_name = "Yahoo"
        api_base = "https://api.login.yahoo.com/oauth/v2/"
        request_token_url = api_base + "get_request_token"
        auth_request_url = api_base + "request_auth"
        access_token_url = api_base + "get_token"
        base_url = "http://fantasysports.yahooapis.com/fantasy/v2/"
        callback_uri = "http://jvh.io"

        if token is None:
            self.oauth = oauth(c_key = consumer_key, c_sec = consumer_secret,
             name = oauth_name, req_tkn_url = request_token_url, 
             auth_url = auth_request_url, acc_tkn_url = access_token_url,
             bs_url = base_url, cb_uri = callback_uri, use_handle = True, 
             json = True)

        else:
            self.oauth = oauth(c_key = consumer_key, c_sec = consumer_secret,
             name = oauth_name, req_tkn_url = request_token_url, 
             auth_url = auth_request_url, acc_tkn_url = access_token_url,
             bs_url = base_url, cb_uri = callback_uri, use_handle = True,
             json = True, tkn = token, tkn_sec = token_secret, handle = handle)
        '''
    
    def __init__(self, client_id, client_secret, token=None):
    
        #OAuth 2.0 Configuration
        oauth_name = "Yahoo"
        api_base = "https://api.login.yahoo.com/oauth2/"
        auth_request_url = api_base + "request_auth"
        access_token_url = api_base + "get_token"
        base_url = "https://fantasysports.yahooapis.com/fantasy/v2/"
        callback_uri = "http://jvh.io"

        if token is None:
            self.oauth = oauth2(c_id = client_id, c_sec = client_secret,
              name = oauth_name, auth_url = auth_request_url, 
              acc_tkn_url = access_token_url, bs_url = base_url,
              cb_uri = callback_uri, json = True, exp = True)

        else:
            self.oauth = oauth2(c_id = client_id, c_sec = client_secret,
              name = oauth_name, auth_url = auth_request_url,
              acc_tkn_url = access_token_url, bs_url = base_url,
              cb_uri = callback_uri, json = True, exp = True,
              refresh_tkn = token)

    def request(self, url_suffix="", debug=False):
        res = self.oauth.request(url_suffix)

        if debug == False:
            res_parsed = json_parse(res, croptop='fantasy_content',
              parse_url = url_suffix)
        else:
            res_parsed = res

        return res_parsed

    def to_dt(self, date_string):
        return dt.strptime(date_string, '%Y-%m-%d')

    def get_ykey(self, key_string):
        return key_string[0:key_string.find('.')]

    def get_seasons(self):
        req = 'games;game_codes=mlb'
        raw = self.request(req)

        ret_list = []
        for i,j in raw.items():
            k = j['game'][0]
            ret_list.append({ 'year' : k['season'], 
              'yahoo_key' : k['game_key'] })

        return sorted(ret_list, key = lambda x : x['year'], reverse=True)

    def get_season(self, year):
        req = 'games;game_codes=mlb;seasons=%s' % str(year)
        raw = self.request(req)

        if len(raw) > 0:
            k = raw['0']['game'][0]
            return [{ 'year' : k['season'], 'yahoo_key' : k['game_key'] }]
        else:
            return []

    def get_leagues(self, season_key):
        req = 'users;use_login=1/games;game_keys=%s/leagues' % season_key
        raw = self.request(req)

        if len(raw) == 0 or 'exception' in raw:
            return {}

        ret_list = []
        for i,j in raw.items():
            k = j['league'][0]
            ret_list.append({ 'name' : k['name'], 'season_key' : season_key,
              'lg_key' : k['league_key'], 'league_id' : k['league_id'], 
              'scoring' : k['scoring_type'], 'teams' : k['num_teams'], 
              'renew' : k['renew'].replace("_", ".l."), 
              'start_dt' : self.to_dt(k['start_date']), 
              'end_dt' : self.to_dt(k['end_date']),
              'weekly' : k['weekly_deadline'] })

        return ret_list

    def get_league(self, league_key):
        req = 'leagues;league_keys=%s' % league_key
        raw = self.request(req)

        k = raw['0']['league'][0]
        return [{ 'name' : k['name'], 'season_key' : self.get_ykey(league_key),
              'lg_key' : k['league_key'], 'league_id' : k['league_id'], 
              'scoring' : k['scoring_type'], 'teams' : k['num_teams'], 
              'renew' : k['renew'].replace("_", ".l."), 
              'start_dt' : self.to_dt(k['start_date']), 
              'end_dt' : self.to_dt(k['end_date']),
              'weekly' : k['weekly_deadline'] }]

    def get_league_settings(self, season_key, league_key):
        req = 'leagues;league_keys=%s.l.%s/settings' % (season_key, league_key)
        raw = self.request(req)

        rosters = []
        for i in raw[0]['roster_positions']:
            rosters.append({ 'pos' : i['roster_position']['position'],
              'type' : i['roster_position']['position_type'],
              'count' : i['roster_position']['count'] })
     
        stats = {}
        for i in raw[0]['stat_categories']['stats']:
            if 'is_only_display_stat' not in i['stat']:
                stats[i['stat']['stat_id']] = { 'disp' : i['stat']['name'],
                  'name' : i['stat']['display_name'], 
                  'type' : i['stat']['position_type'] }

        for i in raw[0]['stat_modifiers']['stats']:
            stats[i['stat']['stat_id']]['value'] = i['stat']['value']
            
        stat_ref = {} #reference dictionary for Abbrev -> Yahoo Stat ID
        for i,j in stats.items():
            stat_ref[j['name']] = i

        return { 'rosters' : rosters, 'stats' : stats, 'stat_ref' : stat_ref,
          'max_teams' : raw[0]['max_teams'],
          'player_pool' : raw[0]['player_pool'],
          'trade_deadline' : raw[0]['trade_end_date'],
          'playoffs' : raw[0]['uses_playoff'],
          'max_games' : raw[1]['max_games_played'],
          'max_innings' : raw[1]['max_innings_pitched'] } 

    def get_league_standings(self, season_key, league_key, stats=False):
        req = 'leagues;league_keys=%s.l.%s/standings' % (season_key, league_key)
        raw = self.request(req)

        raw_standings = raw[0]['teams']
        del(raw_standings['count'])

        standings = []
        for i,j in raw_standings.items():
            std = j['team'][2]['team_standings']
            if stats is True:
                stats = {}
                for k in j['team'][1]['team_stats']['stats']:
                    stats[k['stat']['stat_id']] = {}
                    stats[k['stat']['stat_id']]['val'] = k['stat']['value']
                for k in j['team'][1]['team_points']['stats']:
                    stats[k['stat']['stat_id']]['pts'] = k['stat']['value']

            ret_stnd = { 'team' : j['team'][0][2]['name'],
                    'team_id' : j['team'][0][1]['team_id'],
                    'rank' : std['rank'],
                    'p_for' : std['points_for'],
                    'p_chg' : std['points_change'],
                    'p_bac' : std['points_back'] }
            if stats is True:
                ret_stnd['stats'] = stats

            standings.append(ret_stnd)

        return sorted(standings, key = lambda x: int(x['rank']))

    def get_league_transactions(self, season_key, league_key):
        req = 'leagues;league_keys=%s.l.%s/transactions' % (season_key, 
          league_key)
        raw = self.request(req)

        if len(raw) == 0 or 'exception' in raw:
            return []

        txns = []
        for i,j in raw.items():
            tx = {}
            tx['tx_time'] = \
                dt.fromtimestamp(float(j['transaction'][0]['timestamp']))
            tx['tx_id'] = j['transaction'][0]['transaction_id']
            tx['status'] = j['transaction'][0]['status']
            tx['type'] = j['transaction'][0]['type']

            if 'players' in j['transaction'][1] and \
              'count' in j['transaction'][1]['players']:
                del(j['transaction'][1]['players']['count'])

            if j['transaction'][0]['type'] == 'trade':
                tx['trade'] = []
                for k,l in j['transaction'][1]['players'].items():
                    tx['trade'].append({ 
                      'player_id' : l['player'][0][1]['player_id'],
                      'team_key' : l['player'][1]['transaction_data'][0]\
                        ['source_team_key'],
                      'dest_team_key' : l['player'][1]['transaction_data'][0]\
                        ['destination_team_key'] })
                txns.append(tx)
                   
            elif j['transaction'][0]['type'] != 'commish':
                for k,l in j['transaction'][1]['players'].items():
                    tx_data = l['player'][1]['transaction_data']
                    if len(tx_data) == 1:
                        if tx_data[0]['type'] == 'add':
                            tx['team_key'] = \
                                l['player'][1]['transaction_data'][0]\
                                ['destination_team_key']
                            tx['add'] = {
                              'player_id' : l['player'][0][1]['player_id']} 
                        if tx_data[0]['type'] == 'drop':
                            tx['team_key'] = \
                                l['player'][1]['transaction_data'][0]\
                                ['source_team_key']
                            tx['drop'] = {
                              'player_id' : l['player'][0][1]['player_id']} 
                    else:
                        if tx_data['type'] == 'add':
                            tx['team_key'] = \
                                l['player'][1]['transaction_data']\
                                ['destination_team_key']
                            tx['add'] = {
                              'player_id' : l['player'][0][1]['player_id']} 
                        if tx_data['type'] == 'drop':
                            tx['team_key'] = \
                                l['player'][1]['transaction_data']\
                                ['source_team_key']
                            tx['drop'] = {
                              'player_id' : l['player'][0][1]['player_id']}

                txns.append(tx)

        return sorted(txns, key = lambda x: int(x['tx_id']))
               
    def get_teams(self, season_key, league_key):
        req = 'leagues;league_keys=%s.l.%s/teams' % (season_key, league_key)
        raw = self.request(req)

        if len(raw) == 0 or 'exception' in raw:
            return []

        ret_list = []
        for i,j in raw.items():
            k = j['team'][0]
            m = k[19]['managers'][0]['manager']
            ret_list.append({ 'name' : k[2]['name'], 'team_id' : k[1]['team_id'],
              'manager' : m['nickname'], 'manager_email' : m['email'] })

        return ret_list

    def get_team(self, season_key, league_key, team_key):
        req = 'teams;team_keys=%s.l.%s.t.%s' % (season_key, league_key, 
          team_key)
        raw = self.request(req)

        k = raw['0']['team'][0]
        m = k[19]['managers'][0]['manager']
        return { 'name' : k[2]['name'], 'team_id' : k[1]['team_id'],
          'manager' : m['nickname'], 'manager_email' : m['email'] }

    def get_team_roster(self, season_key, league_key, team_key, date=None):
        req = 'teams;team_keys=%s.l.%s.t.%s/roster' % (season_key, league_key, 
          team_key)
        if date is not None:
            req += ';type=date;date=%s' % date
        raw = self.request(req)

        plyrs = raw['0']['players']
        del(plyrs['count'])

        roster = []
        for i,j in plyrs.items():
            if 'status' in j['player'][0][3]:
                status = j['player'][0][3]['status']
            else:
                status = 'Active'

            roster.append({ 'p_id' : j['player'][0][1]['player_id'], 
              'status' : status,
              'pos' : j['player'][1]['selected_position'][1]['position'] })

        return roster

    def get_team_roster_stats(self, season_key, league_key, team_key, date):
        req = 'teams;team_keys=%s.l.%s.t.%s/roster' % (season_key, league_key, 
          team_key)
        req += ';type=date;date=%s/players/stats' % date
        raw = self.request(req)

        plyrs = raw['0']['players']
        del(plyrs['count'])

        ros_stats = []
        for i,j in plyrs.items():
            if 'status' in j['player'][0][3]:
                status = j['player'][0][3]['status']
            else:
                status = 'Active'

            stats = {} 
            if 'player_stats' in j['player'][3]:
                for k in j['player'][3]['player_stats']['stats']:
                     stats[k['stat']['stat_id']] = k['stat']['value']
            else:
                for k in j['player'][4]['player_stats']['stats']:
                     stats[k['stat']['stat_id']] = k['stat']['value']

            ros_stats.append({ 'id' : j['player'][0][1]['player_id'],
                'stats' : stats})

        return {'roster' : ros_stats, 'date' : to_dt(date)}

    def get_players(self, season_key, league_key, db_get=False):
        req = 'leagues;league_keys=%s.l.%s/players' % (season_key, league_key)
            
        raw_plyrs = []
        plyr_qry = self.request(req)
        if db_get == True:
            print("Fetching players 1-25")
        for i,j in plyr_qry.items():
            raw_plyrs.append(j['player'][0])

        pg_cnt = 1
        while True:
            starter = 25 * pg_cnt
            plyr_qry = self.request(req + ';start=' + str(starter))

            if len(plyr_qry) == 0:
                break

            if db_get == True:
                print("Fetching players " + str(starter + 1) + "-" + \
                  str(starter + len(plyr_qry)))
                
            for i,j in plyr_qry.items():
                raw_plyrs.append(j['player'][0])

            pg_cnt += 1            

        ret_plyrs = []
        for i in raw_plyrs:
            p_id = i[1]['player_id']
            name = i[2]['name']['full']
            if 'status' in i[3]:
                status = i[3]['status']
                if status[0:2] == 'IL':
                    off = 1
                else:
                    off = 0
                team_name = i[6+off]['editorial_team_full_name']
                team_abbr = i[7+off]['editorial_team_abbr']
                elig_pos = i[9+off]['display_position']
                pos_type = i[12+off]['position_type']
            else:
                status = 'Active'
                team_name = i[5]['editorial_team_full_name']
                team_abbr = i[6]['editorial_team_abbr']
                elig_pos = i[8]['display_position']
                pos_type = i[11]['position_type']

            ret_plyrs.append({"p_id" : p_id, "name" : name,"status" : status, 
              "team_name": team_name, "team_abbr" : team_abbr, 
              "pos" : elig_pos, "pos_type" :  pos_type})

        return ret_plyrs

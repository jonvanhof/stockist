from datetime import datetime as dt

class teams():
    def __init__(self, db, yfs, mdl, season_key, league_key, tx_type=None):
        self.yfs = yfs
        self.mdl = mdl
        self.db = db
        self.s_key = season_key
        self.lg_key = league_key
        self.tx_type = tx_type

    def pull(self, refresh=False):
        q_time = dt.now()
        ret_res = []
        if self.tx_type is None:
            q_res = self.db.get(self.mdl, {'lg_key' : self.s_key + ".l." + 
              self.lg_key})
        else:
            q_res = self.db.get(self.mdl, {'lg_key' : self.s_key + ".l." + 
              self.lg_key, 'tx_type' : self.tx_type})
    
        if len(q_res) > 0:
            if refresh == True:
                ret_res = self.stock(q_time, restock=True)
            else:
                ret_res = q_res
        else:
            ret_res = self.stock(q_time)

        for i in ret_res:
            if 'refresh_dt' in i:
                del(i['refresh_dt'])

        return ret_res

    def stock(self, q_time, restock=False):
    	w_res = self.yfs.get_league_transactions(season_key = self.s_key, 
            league_key = self.lg_key)

        txn_dicts = w_res
        put_dicts = []
        for i in txn_dicts:
            np = {}
            np['lg_key'] = self.s_key + ".l." + self.lg_key
            np['season_key'] = self.s_key
            np['league_id'] = self.lg_key
    	    np['refresh_dt'] = q_time
            np['tx_id'] = i['tx_id']
            np['tx_time'] = i['tx_time']
            np['status'] = i['status']
            if i['type'] == 'add/drop':
                np['team_key'] = i['team_key']
                np['team_id'] = i['team_key'].split('.')[4]
                for j in ['add', 'drop']:
                    nadp = np.copy()
                    nadp['tx_type'] = j
                    nadp['player_id'] = i[j]['player_id']
                    if j == 'drop':
                        nadp['tx_line'] = 1
                    else:
                        nadp['tx_line'] = 2
                    put_dicts.append(nadp)
            elif i['type'] == 'trade':
                tx_l = 0
                for j in i['trade']:
                    ntp = np.copy()
                    ntp['tx_type'] = 'trade'
                    ntp['team_key'] = j['team_key']
                    ntp['dest_team_key'] = j['dest_team_key']
                    ntp['team_id'] = j['team_key'].split('.')[4]
                    ntp['player_id'] = j['player_id']
                    ntp['tx_line'] = tx_l
                    tx_l += 1
                    put_dicts.append(ntp)
            else:
                    np['tx_type'] = i['type']
                    np['player_id'] = i[i['type']]['player_id']
                    np['team_key'] = i['team_key']
                    np['team_id'] = i['team_key'].split('.')[4]
                    np['tx_line'] = 1
                    put_dicts.append(np)

    	if restock == True:
    	    self.db.put(self.mdl, put_dicts, update = True)
        else:
    	    self.db.put(self.mdl, put_dicts)

    	return w_res
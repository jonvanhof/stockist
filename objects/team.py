from datetime import datetime as dt

class team():
    def __init__(self, db, yfs, mdl, season_key, league_key, team_id=None):
        self.yfs = yfs
        self.mdl = mdl
        self.db = db
        self.s_key = season_key
        self.lg_key = league_key
        self.team_id = team_id

    def pull(self, refresh=False):
        q_time = dt.now()
        ret_res = []
        if self.team_id is None:
            q_res = self.db.get(self.mdl, {'lg_key' : self.s_key + ".l." + 
              self.lg_key})
        else:
            q_res = self.db.get(self.mdl, {'lg_key' : self.s_key + ".l." + 
              self.lg_key, 'team_id' : self.team_id})
    
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
        w_res = self.yfs.get_teams(self.s_key, self.lg_key)

        put_dicts = w_res
        for i in put_dicts:
            i['lg_key'] = self.s_key + ".l." + self.lg_key
            i['season_key'] = self.s_key
            i['league_id'] = self.lg_key
            i['refresh_dt'] = q_time

        if restock == True:
    	    self.db.put(self.mdl, put_dicts, update = True)
        else:
    	    self.db.put(self.mdl, put_dicts)

        return w_res

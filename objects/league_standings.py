from datetime import datetime as dt

class league_standings():
    def __init__(self, db, yfs, mdl, season_key, league_key, stnd_dt=None):
        self.yfs = yfs
        self.mdl = mdl
        self.db = db
        self.s_key = season_key
        self.lg_key = league_key
        if stnd_dt == None:
            self.stnd_dt = dt.today().date()
        else:
            self.stnd_dt = dt.strptime(stnd_dt, "%m%d%y")

    def pull(self, refresh=False):
        q_time = dt.now()
        ret_res = []
        q_res = self.db.get(self.mdl, {'lg_key' : self.s_key + ".l." + 
            self.lg_key, 'dt' : self.stnd_dt}, o_by="rank.a")
        if len(q_res) > 0:
            for i in q_res:
                if i['refresh_dt'] + self.mdl.stale < q_time \
                  or refresh == True:
                    self.dt = i['dt']
                    ret_res.append(self.stock(q_time, restock=True)[0])
                else:
                    ret_res.append(i)
        else:
            ret_res = self.stock(q_time)

        for i in ret_res:
            if 'refresh_dt' in i:
                del(i['refresh_dt'])

        return ret_res

    def stock(self, q_time, restock=False):
        w_res = self.yfs.get_league_standings(season_key = self.s_key, 
            league_key = self.lg_key)

        put_dicts = w_res
        for i in put_dicts:
            i['lg_key'] = self.s_key + ".l." + self.lg_key
            i['season_key'] = self.s_key
            i['league_id'] = self.lg_key
            i['refresh_dt'] = q_time
            i['dt'] = self.stnd_dt
            #del(i['stats'])
    	
        if restock == True:
    	    self.db.put(self.mdl, put_dicts, update = True)
        else:
    	    self.db.put(self.mdl, put_dicts)

        return w_res

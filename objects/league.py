from datetime import datetime as dt

class league():
    def __init__(self, db, yfs, mdl, season_key, league_key=None):
	    self.yfs = yfs
	    self.mdl = mdl
	    self.db = db
	    self.s_key = season_key
	    self.lg_key = league_key

    def pull(self, refresh=False):
        q_time = dt.now()
        ret_res = []
        if self.lg_key is None:
            q_res = self.db.get(self.mdl, {'season_key' : self.s_key})
            if len(q_res) > 0:
            	for i in q_res:
                    if i['refresh_dt'] + self.mdl.stale < q_time \
                      or refresh == True:
                          self.lg_key = i['league_id']
                          ret_res.append(self.stock(q_time, restock=True)[0])
                    else:
                        ret_res.append(i)
            else:
                ret_res = self.stock(q_time)
            self.lg_key = None
        else:
            q_res = self.db.get(self.mdl, {'season_key' : self.s_key, 
              'league_id' : self.lg_key})
            if len(q_res) > 0:
                if q_res[0]['refresh_dt'] + self.mdl.stale < q_time \
                  or refresh == True:
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
        if self.lg_key is None:
            w_res = self.yfs.get_leagues(season_key=self.s_key)
        else:
            w_res = self.yfs.get_league(league_key=self.s_key + ".l." + 
              self.lg_key)

        put_dicts = w_res
        for i in put_dicts:
    	    i['refresh_dt'] = q_time
    	
        if restock == True:
    	    self.db.put(self.mdl, put_dicts, update = True)
        else:
    	    self.db.put(self.mdl, put_dicts)

        return w_res

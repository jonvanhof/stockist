from datetime import datetime as dt

class season():
    def __init__(self, db, yfs, mdl, year=None):
	    self.yfs = yfs
	    self.mdl = mdl
	    self.db = db
	    self.year = year

    def pull(self, refresh=False):
        q_time = dt.now()
        ret_res = []

        if self.year is None:
            q_res = self.db.get(self.mdl, o_by="year.d")
            if len(q_res) > 0:
                for i in q_res:
                    if q_res[0]['refresh_dt'] + self.mdl.stale < q_time \
                      or refresh == True:
                        self.year = i['year']
                        ret_res = self.stock(q_time, restock=True)
                    else:
                        ret_res.append(i)
            else:
        	    ret_res = self.stock(q_time)
            self.year = None
        else:
            q_res = self.db.get(self.mdl, {'year' : self.year})
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
        if self.year is None:
            w_res = self.yfs.get_seasons()
        else:
    	    w_res = self.yfs.get_season(year=self.year)

        put_dicts = w_res
        for i in put_dicts:
    	    i['refresh_dt'] = q_time
        if restock == True:
    	    self.db.put(self.mdl, put_dicts, update = True)
        else:
    	    self.db.put(self.mdl, put_dicts)

        return w_res

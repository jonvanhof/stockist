from datetime import datetime as dt

class proj_zips():
    def __init__(self, db, zps, mdl, year=None):
        self.zps = zps
        self.mdl = mdl
        self.db = db
        if year is None:
            self.yr = str(dt.today().year)
        else:
            self.yr = year

    def pull(self, p_id=None, refresh=False):
        ret_res = []
        if p_id == None:
            q_res = self.db.get(self.mdl, {'yr' : self.yr})
        else:
            q_res = self.db.get(self.mdl, {'yr' : self.yr, 'playerid' : p_id})
        if len(q_res) > 0:
            for i in q_res:
                if refresh == True:
                    ret_res.append(self.stock(restock=True)[0])
                else:
                    ret_res.append(i)
        else:
            ret_res = self.stock()

        return ret_res

    def stock(self, restock=False):
        w_res = self.zps.read()

        put_dicts = w_res
        for i in put_dicts:
            i['yr'] = self.yr
    	
        if restock == True:
    	    self.db.put(self.mdl, put_dicts, update = True)
        else:
    	    self.db.put(self.mdl, put_dicts)

        return w_res

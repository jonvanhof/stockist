from datetime import datetime as dt
from util.stk_match import mtch_nm

class player():
    def __init__(self, db, yfs, mdl, season_key, league_key, player_id=None):
        self.yfs = yfs
        self.mdl = mdl
        self.db = db
        self.s_key = season_key
        self.lg_key = league_key
        if player_id is not None:
            self.p_id = str(player_id)

    def pull(self, p_id=None, refresh=False):
        q_time = dt.now()
        ret_res = []
        if p_id is None:
            q_res = self.db.get(self.mdl)
            if len(q_res) > 0:
                if refresh == True:
                    ret_res = self.stock(q_time, restock=True)
                else:
                    ret_res = q_res
            else:
                ret_res = self.stock(q_time)
        else:
            self.p_id = str(p_id)
            q_res = self.db.get(self.mdl, { 'p_id' : self.p_id })
            ret_res = q_res
            self.p_id = None

        for i in ret_res:
            if 'refresh_dt' in i:
                del(i['refresh_dt'])

        return ret_res

    def stock(self, q_time, restock=False):
        w_res = self.yfs.get_players(season_key = self.s_key, 
          league_key = self.lg_key)

        txn_dicts = w_res
        put_dicts = []
        for i in txn_dicts:
            np = i
            put_dicts.append(np)

        if restock == True:
    	    self.db.put(self.mdl, put_dicts, update = True)
        else:
    	    self.db.put(self.mdl, put_dicts)

        return w_res

    def upd_zips(self, o_z):
        q_res = self.db.get(self.mdl)
        zps = o_z.pull()
        put_dicts = []

        for i in q_res:
            if i['zips_id'] is None:
                for j in zps:
                    if mtch_nm(i['name'], j['name']) == True:
                        if (i['pos_type'] == 'B' and j['PA'] is not None) or \
                          (i['pos_type'] == 'P' and j['ERA'] is not None):
                            i['zips_id'] = j['playerid']
                            put_dicts.append(i)
                            break
                        
        print(len(put_dicts))
        self.db.put(self.mdl, put_dicts, update = True)

    def upd_mlb(self, mlb):
        q_res = self.db.get(self.mdl)
        put_dicts = []

        for i in q_res:
            if i['mlb_id'] is None:
                mlb_plyr = mlb.get_player(i['name'])
                if len(mlb_plyr) > 0:
                    for j in mlb_plyr:
                        if (i['pos_type'] == 'B' and j['pos'] != 'P') or \
                          i['pos_type'] == 'P' and j['pos'] == 'P' or \
                          '(Batter)' in i['name']:
                            i['mlb_id'] = j['id']
                            i['birth_date'] = j['birth_dt']
                            put_dicts.append(i)
                        
        print(len(put_dicts))
        self.db.put(self.mdl, put_dicts, update = True)

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class datastore:
    def __init__(self, user, passwd, host, port, db):
        self.eng = sa.create_engine("postgresql+psycopg2://%s:%s@%s:%s/%s" %
                                    (user, passwd, host, port, db))
        self.eng.connect()
        self.session = sessionmaker(bind=self.eng)()
        self.base = declarative_base

    def create_tbl(self):
        self.base.metadata.create_all(self.eng)

    def drop_tbl(self):
        self.base.metadata.drop_all(self.eng)

    def set_base(self, base):
        self.base = base

    def get(self, model, q_filter=None, o_by=None):
        ret_list = []
        if o_by is not None and q_filter is None:
            col, srt = o_by.split(".")
            mdl_srt = getattr(model, col)
            if srt == "d":
                raw_res = self.session.query(model).order_by(mdl_srt.desc())\
                  .all()
            else:
                raw_res = self.session.query(model).order_by(mdl_srt).all()
        elif q_filter is None:
            raw_res = self.session.query(model).all()
        else:
            if o_by is not None:
                col, srt = o_by.split(".")
                mdl_srt = getattr(model, col)
                if srt == "d":
                    raw_res = self.session.query(model)\
                      .filter_by(**(q_filter)).order_by(mdl_srt.desc()).all()
                else:
                    raw_res = self.session.query(model)\
                      .filter_by(**(q_filter)).order_by(mdl_srt).all()
            else:
                raw_res = self.session.query(model).filter_by(**(q_filter))\
                  .all()

        for i in raw_res:
            res_dict = i.__dict__
            del(res_dict['_sa_instance_state'])
            ret_list.append(res_dict)

        return ret_list

    def put(self, model, put_dicts, update=False):
        if not update:
            put_mdls = []
            for i in put_dicts:
                put_mdls.append(model(**i))
            self.session.add_all(put_mdls)
        else:
            pks = []
            for i in sa.inspect(model).primary_key:
                pks.append(i.name)
            for i in put_dicts:
                pk = {}
                for j in pks:
                    pk[j] = i[j]
                res_cnt = self.session.query(model).filter_by(**pk).count()
                if res_cnt == 0:
                    self.session.add(model(**i))
                else:
                    self.session.query(model).filter_by(**pk).update(i)
        
        self.session.commit()

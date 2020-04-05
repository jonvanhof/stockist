from sqlalchemy import Column, String, Integer, DateTime
from .base import mdl_base

class proxy(mdl_base):
    __tablename__ = "proxy"
    __table_args__ = {"schema" : "gerente"}

    league_key = Column(String, primary_key=True)
    prx_p_id = Column(Integer, primary_key=True)
    name = Column(String)
    team_id = Column(Integer)
    mlb_id = Column(Integer)
    birth_dt = Column(DateTime)

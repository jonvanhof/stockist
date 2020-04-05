from sqlalchemy import Column, Integer, String, DateTime
from datetime import timedelta as td
from .base import mdl_base

class player(mdl_base):
    __tablename__ = "player"
    __table_args__ = {"schema" : "gerente"}

    p_id = Column(String, primary_key=True)
    pos_type = Column(String, primary_key=True)
    mlb_id = Column(String)
    zips_id = Column(String)
    name = Column(String)
    team_name = Column(String)
    team_abbr = Column(String)
    birth_date = Column(DateTime)
    pos = Column(String)
    status = Column(String)
    refresh_dt = Column(DateTime)

    stale = td(days=30)

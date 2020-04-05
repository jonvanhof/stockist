from sqlalchemy import Column, Integer, String, DateTime
from datetime import timedelta as td
from .base import mdl_base

class roster(mdl_base):
    __tablename__ = "roster"
    __table_args__ = {"schema" : "gerente"}

    lg_key = Column(String, primary_key=True)
    team_id = Column(Integer, primary_key=True)
    p_id = Column(Integer, primary_key=True)
    roster_dt = Column(DateTime, primary_key=True)
    pos = Column(String)
    status = Column(String)
    season_key = Column(String)
    league_id = Column(String)
    refresh_dt = Column(DateTime)

    stale = td(days=1)

from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import timedelta as td
from .base import mdl_base

class league_standings(mdl_base):
    __tablename__ = "league_standings"
    __table_args__ = {"schema" : "gerente"}

    lg_key = Column(String, primary_key=True)
    dt = Column(DateTime, primary_key=True)
    team_id = Column(Integer, primary_key=True)
    season_key = Column(String)
    league_id = Column(String)
    team = Column(String)
    p_for = Column(Float(precision=2))
    p_bac = Column(Float(precision=2))
    p_chg = Column(Float(precision=2))
    rank = Column(Integer)
    refresh_dt = Column(DateTime)

    stale = td(days=1)

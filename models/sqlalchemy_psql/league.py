from sqlalchemy import Column, Integer, String, DateTime
from datetime import timedelta as td
from .base import mdl_base

class league(mdl_base):
    __tablename__ = "league"
    __table_args__ = {"schema" : "gerente"}

    lg_key = Column(String, primary_key=True)
    season_key = Column(String)
    league_id = Column(String)
    name = Column(String)
    teams = Column(Integer)
    scoring = Column(String)
    renew = Column(String)
    start_dt = Column(DateTime)
    end_dt = Column(DateTime)
    weekly = Column(String)
    refresh_dt = Column(DateTime)

    stale = td(days=30)

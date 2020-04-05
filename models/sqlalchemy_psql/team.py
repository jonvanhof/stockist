from sqlalchemy import Column, Integer, String, DateTime
from datetime import timedelta as td
from .base import mdl_base

class team(mdl_base):
    __tablename__ = "team"
    __table_args__ = {"schema" : "gerente"}

    lg_key = Column(String, primary_key=True)
    team_id = Column(Integer, primary_key=True)
    season_key = Column(String)
    league_id = Column(String)
    name = Column(String)
    manager = Column(String)
    manager_email = Column(String)
    refresh_dt = Column(DateTime)

    stale = td(days=365)

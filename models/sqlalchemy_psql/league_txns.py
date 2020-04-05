from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import timedelta as td
from .base import mdl_base

class league_txns(mdl_base):
    __tablename__ = "league_txns"
    __table_args__ = {"schema" : "gerente"}

    lg_key = Column(String, primary_key=True)
    tx_id = Column(Integer, primary_key=True)
    tx_line = Column(Integer, primary_key=True)
    tx_time = Column(DateTime)
    status = Column(String)
    team_key = Column(String)
    dest_team_key = Column(String)
    season_key = Column(String)
    league_id = Column(String)
    team_id = Column(Integer)
    tx_type = Column(String)
    player_id = Column(Integer)
    refresh_dt = Column(DateTime)

    stale = td(days=1)

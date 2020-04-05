from sqlalchemy import Column, String, Integer
from .base import mdl_base

class team_change(mdl_base):
    __tablename__ = "team_change"
    __table_args__ = {"schema" : "gerente"}

    league_key = Column(String, primary_key=True)
    team_id = Column(Integer, primary_key=True)
    league_key_prev = Column(String)
    team_id_prev = Column(Integer)

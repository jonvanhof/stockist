from sqlalchemy import Column, String, Integer
from .base import mdl_base

class passer(mdl_base):
    __tablename__ = "passer"
    __table_args__ = {"schema" : "gerente"}

    league_key = Column(String, primary_key=True)
    team_id = Column(Integer, primary_key=True)
    round_num = Column(Integer)

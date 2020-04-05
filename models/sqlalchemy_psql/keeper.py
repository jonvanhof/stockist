from sqlalchemy import Column, String, Integer
from .base import mdl_base

class keeper(mdl_base):
    __tablename__ = "keeper"
    __table_args__ = {"schema" : "gerente"}

    league_key = Column(String, primary_key=True)
    p_id = Column(String, primary_key=True)
    team_id = Column(Integer)

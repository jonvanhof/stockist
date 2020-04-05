from sqlalchemy import Column, Integer, String, DateTime
from datetime import timedelta as td
from .base import mdl_base

class season(mdl_base):
    __tablename__ = "season"
    __table_args__ = {"schema" : "gerente"}

    year = Column(Integer, primary_key=True)
    yahoo_key = Column(String)
    refresh_dt = Column(DateTime)

    stale = td(days=365)

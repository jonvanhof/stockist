from sqlalchemy import Column, String, Integer
from .base import mdl_base

class bad_txn(mdl_base):
    __tablename__ = "bad_txn"
    __table_args__ = {"schema" : "gerente"}

    league_key = Column(String, primary_key=True)
    tx_id = Column(Integer, primary_key=True)

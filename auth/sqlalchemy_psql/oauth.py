from sqlalchemy import Column, String
from .base import auth_base

class profile(auth_base):
    __tablename__ = "profile"
    __table_args__ = {"schema" : "gerente"}

    username = Column(String, primary_key=True)
    provider = Column(String, primary_key=True)
    token = Column(String)
    token_secret = Column(String)
    handle = Column(String)
    refresh_token = Column(String)

class provider(auth_base):
    __tablename__ = "provider"
    __table_args__ = {"schema" : "gerente"}

    provider = Column(String, primary_key=True)
    consumer_key = Column(String)
    consumer_secret = Column(String)

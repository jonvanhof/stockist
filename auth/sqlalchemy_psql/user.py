from sqlalchemy import Column, String
from .base import auth_base

class user(auth_base):
    __tablename__ = "user"
    __table_args__ = {"schema" : "gerente"}

    username = Column(String, primary_key=True)
    password = Column(String)

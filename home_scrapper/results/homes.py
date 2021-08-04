# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Homes(Base):
    __tablename__ = "homes"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    city = Column(String)
    neighbourhood = Column(String)
    price = Column(Float)
    currency = Column(String)
    year = Column(Integer)
    sqm = Column(Float)
    floor = Column(Integer)
    rooms = Column(Integer)
    heating = Column(String)
    url = Column(String, unique=True)

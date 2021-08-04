# -*- coding: utf-8 -*-
from sqlalchemy import create_engine

from .homes import Homes

# db_engine = create_engine('sqlite:///:memory:')
db_engine = create_engine("sqlite:///data/data.db")  # echo = True
Homes.metadata.create_all(db_engine)

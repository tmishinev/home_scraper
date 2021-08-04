# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session

from home_scrapper.results import db
from home_scrapper.results import Homes

session = Session(bind=db)
res = session.query(Homes).all()

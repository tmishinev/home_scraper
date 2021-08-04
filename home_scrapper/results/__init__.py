# -*- coding: utf-8 -*-
from .homes import Homes
from home_scrapper import db

Homes.metadata.create_all(db)

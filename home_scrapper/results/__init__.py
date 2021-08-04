# -*- coding: utf-8 -*-
from sqlalchemy import create_engine

from .homes import Homes
from home_scrapper import data_dir


# define DB path and remove if DB exists
_db_path = data_dir / "data.db"
_db_path.unlink(missing_ok=True)

# create db engine
# db = create_engine('sqlite:///:memory:', echo = True)
db = create_engine(f"sqlite:///{_db_path}")
Homes.metadata.create_all(db)

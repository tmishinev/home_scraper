# -*- coding: utf-8 -*-
from pathlib import Path

from sqlalchemy import create_engine

__version__ = "0.1.0"

# set data directory
data_dir = Path(__file__).parent.parent / "data"
if not data_dir.exists():
    data_dir.mkdir(parents=True)

# set DB path
_db_path = data_dir / "data.db"
_db_path.unlink(missing_ok=True)  # TODO: this should be handled somehow

# create DB engine
# db = create_engine('sqlite:///:memory:', echo = True)
db = create_engine(f"sqlite:///{_db_path}")

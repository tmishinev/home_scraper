# -*- coding: utf-8 -*-
import logging

import pandas as pd
from sqlalchemy.orm import Session

from home_scrapper.results import db
from home_scrapper.results import Homes


logger = logging.getLogger(__name__)


def get_objects():
    session = Session(bind=db)
    return session.query(Homes).all()


def main():
    """Runner script for the scrapper!"""

    # analyse data
    df = pd.read_sql_query("SELECT * FROM homes;", con=db)
    print("-" * 40)
    print(f"Average price: {df.describe().loc['mean', 'price']:.2f} EUR")
    print(f"Number of properties: {df.shape[0]}")


if __name__ == "__main__":
    main()

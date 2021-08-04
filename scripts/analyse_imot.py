# -*- coding: utf-8 -*-
import logging

import pandas as pd
from sqlalchemy.orm import Session

from home_scrapper.results import db
from home_scrapper.results import Homes


logger = logging.getLogger(__name__)


def query_homes():
    """Returns all home rows (objects) in the DB!"""
    session = Session(bind=db)
    return session.query(Homes).all()


def query_urls():
    """Returns iterable of all urls!"""
    session = Session(bind=db)
    return session.query(Homes.title, Homes.url)


def main():
    """Runner script for the scrapper!"""

    # analyse data
    df = pd.read_sql_query("SELECT * FROM homes;", con=db)
    print("-" * 40)
    print(f"Average price: {df.describe().loc['mean', 'price']:.2f} EUR")
    print(f"Number of properties: {df.shape[0]}")

    # query objects
    for home in query_homes():
        print(f"{home.title}: {home.url}")

    # query all urls
    for title, url in query_urls():
        print(f"{title}: {url}")


if __name__ == "__main__":
    main()

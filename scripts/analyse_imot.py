# -*- coding: utf-8 -*-
import datetime
import logging
import webbrowser

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


def main(days_back: int = 0):
    """Runner script for the scrapper!"""

    # set reference date
    reference_date = datetime.date.today() - datetime.timedelta(days=days_back)

    # query objects
    homes = query_homes()
    for home in homes:

        # print objects updated today
        if home.last_updated is not None and home.last_updated.date() >= reference_date:
            print(home.city, home.title, home.url)
            webbrowser.open_new_tab(home.url)

        # print objects from today
        if home.created.date() >= reference_date:
            print(home.created.date(), home.city, home.url)
            webbrowser.open_new_tab(home.url)

    # analyse data
    # df = pd.read_sql_query("SELECT * FROM homes;", con=db)
    df = pd.DataFrame([vars(home) for home in homes])
    print("-" * 40)
    print(f"Average price: {df.describe().loc['mean', 'price']:.2f} EUR")
    print(f"Number of properties: {df.shape[0]}")


if __name__ == "__main__":
    main()

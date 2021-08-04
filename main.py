# -*- coding: utf-8 -*-
import logging

import pandas as pd

from home_scrapper.results import db
from home_scrapper.scrapers import ImotScraper


logger = logging.getLogger(__name__)


def main():
    """Runner script for the scrapper!"""

    # run scrapper on the following search result urls
    urls = {
        "Sofia": "https://www.imot.bg/pcgi/imot.cgi?act=3&slink=6sn5gf&f1=1",
        "Plovdiv": "https://www.imot.bg/pcgi/imot.cgi?act=3&slink=6sq759&f1=1",
    }
    for city, url in urls.items():
        print("=" * 40)
        print(f"Processing data from {city}:")
        scraper = ImotScraper(url=url)
        scraper.run(sleep=5)

    # analyse data
    df = pd.read_sql_query("SELECT * FROM homes;", con=db)
    print("-" * 40)
    print(f"Average price: {df.describe().loc['mean', 'price']:.2f} EUR")
    print(f"Number of properties: {df.shape[0]}")


if __name__ == "__main__":
    main()

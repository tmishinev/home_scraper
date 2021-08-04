# -*- coding: utf-8 -*-
import datetime
import logging

from home_scrapper import data_dir
from home_scrapper.scrapers import ImotScraper

logger = logging.getLogger(__name__)


def main(url: str, sleep: int = 5):
    """Runner script for the scrapper!

    :param url: target URL
    :param sleep: sleep time between URL requests"""

    # run scrapper
    scraper = ImotScraper(url=url)
    scraper.run(sleep=sleep)


if __name__ == "__main__":

    # Passing the following url to the scraper returns the
    # search results for the following search criteria:
    # - sofia
    # - from 2 rooms to attic
    # - price <= 130000 EUR
    # - area>70sqm
    # - year<=1990
    # - floor>=2
    # - bricks
    # Note that the last number in the url defines the page number (e.g. f1=1 corresponds to the first page).

    # set destination file path
    now = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    dest_filename = data_dir / f"data_{now}.csv"

    # run scrapper on the following search result urls
    urls = {
        "Sofia": "https://www.imot.bg/pcgi/imot.cgi?act=3&slink=6sn5gf&f1=1",
        "Plovdiv": "https://www.imot.bg/pcgi/imot.cgi?act=3&slink=6sq759&f1=1",
    }
    for city, url in urls.items():
        print("=" * 40)
        print(f"Processing data from {city}:")
        main(url=url)

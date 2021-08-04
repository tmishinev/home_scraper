# -*- coding: utf-8 -*-
import logging

from home_scrapper.scrapers import ImotScraper
from home_scrapper import data_dir


logger = logging.getLogger(__name__)


def main(url: str):

    # run scrapper
    scraper = ImotScraper(url=url)
    scraper.run(sleep=5)

    # export to csv
    scraper.to_csv(filename=data_dir / "data.csv")

    # check data
    df = scraper.get_scraped_data()
    df = df.astype({"price": float})

    # calculate some stats
    print(f"Average price in EUR: {df.describe().loc['mean', 'price']}")
    print(f"Number of properties: {df.shape[0]}")


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

    main(url="https://www.imot.bg/pcgi/imot.cgi?act=3&slink=6sn5gf&f1=1")

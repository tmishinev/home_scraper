# -*- coding: utf-8 -*-
import logging

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


if __name__ == "__main__":
    main()

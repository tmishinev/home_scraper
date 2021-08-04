# -*- coding: utf-8 -*-
import logging
import random

from home_scrapper.scrapers import ImotScraper


logger = logging.getLogger(__name__)


def main(headers: dict, urls: dict):
    """Runner script for the scrapper!"""

    # run scrapper on the following search result urls
    for city, url in urls.items():
        print("=" * 40)
        print(f"Processing data from {city}:")
        scraper = ImotScraper(url=url, headers=headers)
        scraper.run(sleep=random.uniform(1.5, 2.9))


if __name__ == "__main__":
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0",
    }
    urls = {
        "Sofia": "https://www.imot.bg/pcgi/imot.cgi?act=3&slink=6ufg52&f1=1",
        "Plovdiv": "https://www.imot.bg/pcgi/imot.cgi?act=3&slink=6uffou&f1=1",
    }
    main(headers=headers, urls=urls)

# -*- coding: utf-8 -*-
import logging

from home_scrapper.scrapers import ImotScraper


logger = logging.getLogger(__name__)


def main(
    headers: dict, urls: dict, params: dict = None, sleep_range: tuple = (1.5, 2.9)
):
    """Runner script for the scrapper!

    :param headers: browser header used by the requests package
    :param urls: city name and search result urls
    :param params: browser parameters used by the requests package
    :param sleep_range: range for the sleep time
    """

    # run scrapper on the following search result urls
    for city, url in urls.items():
        print("=" * 40)
        print(f"Processing data from {city}:")
        scraper = ImotScraper(url=url, headers=headers, params=params)
        scraper.run(sleep_range=sleep_range)


if __name__ == "__main__":
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0",
    }
    urls = {
        "Sofia": "https://www.imot.bg/pcgi/imot.cgi?act=3&slink=6ywpm1&f1=1",
        "Plovdiv": "https://www.imot.bg/pcgi/imot.cgi?act=3&slink=6ywpp6&f1=1",
    }
    main(headers=headers, urls=urls)

    # TODO: 1) run pages in random order
    #       2) fix floor
    #       3) parsing the current HTMLs does not scrape all data as it seems that the results are limited to 25 pages

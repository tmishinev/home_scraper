# -*- coding: utf-8 -*-
import logging
from pathlib import Path

import pandas as pd

from bs4 import BeautifulSoup
from bs4.element import Tag


from home_scrapper.results import Home

from .base import Scraper

logger = logging.getLogger(__name__)


class ImotScraper(Scraper):

    def get_scraped_data(self):
        """Returns the scraped data as pandas DataFrame"""
        df = pd.DataFrame()
        for home in self.homes:
            d = vars(home)
            df = df.append(pd.Series(d), ignore_index=True)
        return df

    @staticmethod
    def _get_price(card: Tag) -> tuple:
        """Returns the price!

        :param card: HTML table tag containing some home details
        """

        div = card.findChildren("div", attrs={"class": "price"})[0]
        dum = div.text.strip()
        price = "".join(c for c in dum if c.isdigit())
        currency = "".join(c for c in dum if not c.isdigit())
        return float(price), currency.strip()

    @staticmethod
    def _get_summary_caption(card):
        """Returns the summary caption from the results page!

        :param card: HTML table tag containing home details
        """

        caption = card.findChildren("td", attrs={"colspan": "3"})[0]
        return caption.text

    @staticmethod
    def _get_title_link(card: Tag) -> tuple:
        """Returns ad title and its corresponding url!

        :param card: HTML table tag containing home details
        """

        title_link = card.findChildren("a", attrs={"class": "lnk1"})[0]
        return title_link.text, "https:" + title_link.attrs["href"]

    @staticmethod
    def _get_location_link(card: Tag) -> tuple:
        """Returns location text and its corresponding url!

        :param card: HTML table tag containing home details
        """
        location_link = card.findChildren("a", attrs={"class": "lnk2"})[0]
        return location_link.text, "https:" + location_link.attrs["href"]

    def _get_room_count(self, card: Tag) -> int:
        """Returns number of rooms!

        :param card: HTML table tag containing home details
        """

        title, _ = self._get_title_link(card)
        rooms = "".join(c for c in title if c.isdigit())
        return int(rooms)

    def _get_location(self, card: Tag) -> tuple:
        """Returns city and neighbourhood names!

        :param card: HTML table tag containing home details
        """
        location, _ = self._get_location_link(card)
        city, neighbourhood = location.split(sep=",")
        return city.strip(), neighbourhood.strip()

    @staticmethod
    def get_page_count(soup):
        """Returns the number of serach result pages!

        :param soup: BeautifulSoup object
        """
        page_number_info = soup.find("span", {"class": "pageNumbersInfo"}).text
        return int(page_number_info.split(sep="от")[-1].strip())

    def scrape(self, card: Tag, sleep: int = 5) -> Home:
        """Extracts the data for each parsed card

        :param card: results card from the web page
        :param sleep: sleep between each scrape"""

        # extract information
        home = Home()
        home.price, home.currency = self._get_price(card)
        home.rooms = self._get_room_count(card)
        home.title, home.url = self._get_title_link(card)
        home.city, home.neighbourhood = self._get_location(card)

        # # request card (ad) page (HTML)
        # # TODO: before each request one should use time.sleep(sleep)
        # response = self.request(url=home.url)
        # soup = BeautifulSoup(response.content, "html.parser")
        # soup.prettify()

        return home

    def run(self, sleep: int = 5):
        """Scraper runner method!

        :param sleep: sleep between each scrape
        """

        # request HTML
        response = self.request(url=self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        soup.prettify()

        # get number of pages
        self.pages = self.get_page_count(soup)

        # get the main table and loop over its children
        td = soup.find("td", {"rowspan": 2})
        cards = td.findChildren("table")
        for card in cards:
            if isinstance(card, Tag):
                # skip adds
                if ["novaSgrada"] in card.attrs.values():
                    continue

                # process flats
                if "style" in card.attrs.keys():
                    if "резултат" in card.text.lower():
                        # TODO: extract card information
                        self.search_params = card.text
                    else:
                        home = self.scrape(card=card, sleep=sleep)
                        self.homes.append(home)

    def to_csv(self, filename: Path):
        """Exports results to a CSV file!

        :param filename: target file path"""

        df = self.get_scraped_data()
        df.to_csv(filename)
        df.to_csv(filename, index=False)

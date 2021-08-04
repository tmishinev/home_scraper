# -*- coding: utf-8 -*-
import logging
import time

import numpy as np
from bs4 import BeautifulSoup
from bs4.element import Tag

from .base import Scraper
from home_scrapper.results import db
from home_scrapper.results import Homes


logger = logging.getLogger(__name__)


class ImotScraper(Scraper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
    def _get_caption(card):
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
        try:
            rooms = int(rooms)
        except ValueError:
            rooms = np.nan
        return rooms

    def _get_location(self, card: Tag) -> tuple:
        """Returns city and neighbourhood names!

        :param card: HTML table tag containing home details
        """
        location, _ = self._get_location_link(card)
        city, neighbourhood = location.split(sep=",")
        return city.strip(), neighbourhood.strip()

    @staticmethod
    def _get_page_count(soup):
        """Returns the number of serach result pages!

        :param soup: BeautifulSoup object
        """
        page_number_info = soup.find("span", {"class": "pageNumbersInfo"}).text
        return int(page_number_info.split(sep="от")[-1].strip())

    def _scrape(self, card: Tag, sleep: float = 3.0):
        """Extracts the data for each parsed card

        :param card: results card from the web page
        :param sleep: sleep between each scrape"""

        # extract information
        home = Homes()
        home.price, home.currency = self._get_price(card)
        home.rooms = self._get_room_count(card)
        home.title, home.url = self._get_title_link(card)
        home.city, home.neighbourhood = self._get_location(card)

        # extract data from the caption
        data = self._get_caption(card)
        captions = data.replace("\n", "").strip().split(sep=",")
        for caption in captions:
            caption = caption.strip().lower()
            if "кв.м" in caption:
                if home.area is None:
                    home.area = caption
            elif "ет." in caption:
                if home.floor is None:
                    home.floor = caption
            elif "г." in caption:
                if home.type is None:
                    home.type = caption
            elif "лок.отопл." == caption or "тец" == caption or "газ" == caption:
                if home.heating is None:
                    home.heating = caption
                else:
                    home.heating += ", " + caption
            elif "тел." in caption:
                if home.phone is None:
                    caption = (
                        caption.replace("-", "")
                        .replace("/", "")
                        .replace(" ", "")
                        .replace("тел.:", "")
                    )
                    home.phone = caption
            else:
                logging.info(f"Skipping caption: {caption}")

        # write to DB
        home.to_db(db)

        # # request card (ad) page (HTML)
        # # TODO: before each request one should use time.sleep(sleep)
        # time.sleep(sleep)
        # response = self.request(url=home.url)
        # soup = BeautifulSoup(response.content, "html.parser")
        # soup.prettify()

    def run(self, sleep: float = 3.0):
        """Scraper runner method!

        :param sleep: sleep between each scrape
        """

        # request HTML
        response = self.request(url=self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        soup.prettify()

        # loop over results pages
        page_count = self._get_page_count(soup)
        for i in range(1, page_count + 1):

            print(f"Scraping result page {i} ... ", end="")

            # request the next page
            if i > 1:
                time.sleep(sleep)
                url = self.url.replace("&f1=1", f"&f1={i}")
                response = self.request(url=url)
                soup = BeautifulSoup(response.content, "html.parser")
                soup.prettify()

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
                            self._scrape(card=card)

            print("done!")

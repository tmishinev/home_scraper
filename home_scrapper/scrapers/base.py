# -*- coding: utf-8 -*-
from abc import ABC

import requests
from requests.models import Response
from sqlalchemy.orm import Session

from home_scrapper.results import db


class Scraper(ABC):
    def __init__(self, url):
        self.homes = []
        self.url = url
        self.headers = {
            "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0",
        }
        self.search_params = ""

        # create DB session
        # TODO: check if leaving this open causes problems!?
        self.session = Session(bind=db)

    def request(self, url: str, params: dict = None) -> Response:
        """Returns a BeatifulSoup object from the parsed url!

        :param url: target url string
        :param params: pagination query parameters
        """
        return requests.get(url, headers=self.headers, params=params)

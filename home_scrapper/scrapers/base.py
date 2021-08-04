# -*- coding: utf-8 -*-
from abc import ABC

import requests
from requests.models import Response


class Scraper(ABC):
    def __init__(self, url: str, headers: dict, params: dict = None):
        """Abstract Scraper class

        :param url: target URL
        :param headers: browser headers to be used when requesting the URL
        :param params: browser params to be used when requesting the URL
        """
        self.homes = []
        self.url = url
        self.headers = headers
        self.params = params
        self.search_params = ""

    def request(self, url: str) -> Response:
        """Returns a BeatifulSoup object from the parsed url!

        :param url: target url string
        """
        return requests.get(url, headers=self.headers, params=self.params)

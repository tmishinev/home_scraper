from abc import ABC

import requests
from requests.models import Response


class Scraper(ABC):

    def __init__(self, url):
        self.homes = []
        self.url = url
        self.headers = {
            "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0",
        }
        self.pages = None
        self.search_params = ""

    def request(self, url: str, params: dict = None) -> Response:
        """Returns a BeatifulSoup object from the parsed url!

        :param url: target url string
        :param params: pagination query parameters
        """
        return requests.get(url, headers=self.headers, params=params)

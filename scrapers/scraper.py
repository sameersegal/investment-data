from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from pydantic import BaseModel
from datetime import datetime
import requests

class PageContent(BaseModel):
    title: str
    body: str
    date: datetime


class Scraper(ABC):

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

    @abstractmethod
    def _get_payload_structure(self):
        raise NotImplementedError('Need to define a playload structure')

    @abstractmethod
    def _get_login_url(self):
        raise NotImplementedError('Need to define a login url')

    @abstractmethod
    def _parse(self, soup):
        raise NotImplementedError('Need to define a parse method')

    def scrape(self, url: str) -> PageContent:
        session = requests.Session()

        s = session.post(self._get_login_url(),
                         data=self._get_payload_structure())

        # Navigate to the next page and scrape the data
        s = session.get(url)

        soup = BeautifulSoup(s.text, 'html.parser')

        content = self._parse(soup)

        if content.title is '' or content.body is '':
            raise Exception(f'Not able to parse the page {url}')

        return content

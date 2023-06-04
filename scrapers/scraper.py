from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from pydantic import BaseModel
from datetime import datetime
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


REQUESTS = 1
SELENIUM = 2


class PageContent(BaseModel):
    title: str
    body: str
    date: datetime


class Scraper(ABC):

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

    def _get_payload_structure(self):
        raise NotImplementedError('Need to define a playload structure')

    def _get_login_url(self):
        raise NotImplementedError('Need to define a login url')

    @abstractmethod
    def _parse(self, soup):
        raise NotImplementedError('Need to define a parse method')

    def _driver_mode(self):
        return REQUESTS

    def _login_via_requests(self):
        session = requests.Session()
        s = session.post(self._get_login_url(),
                         data=self._get_payload_structure())

        return session

    def _login_via_selenium(self):
        # Set Chrome options to enable JavaScript
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--enable-javascript")

        # Create a new instance of the Chrome driver with the options
        driver = webdriver.Chrome(options=chrome_options)

        return driver

    def scrape(self, url: str) -> PageContent:

        driver_mode = self._driver_mode()

        html = ""

        if driver_mode == REQUESTS:

            session = self._login_via_requests()

            # Navigate to the next page and scrape the data
            s = session.get(url)

            html = s.text

        elif driver_mode == SELENIUM:

            driver = self._login_via_selenium()

            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body')))
            time.sleep(10)
            html = driver.page_source

        content = self.parse_html(html)

        if content.title == '' or content.body == '':
            raise Exception(f'Not able to parse the page {url}')

        return content

    def parse_html(self, html) -> PageContent:

        soup = BeautifulSoup(html, 'html.parser')

        content = self._parse(soup)

        return content

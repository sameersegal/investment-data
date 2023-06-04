from .scraper import Scraper, PageContent, SELENIUM
from datetime import datetime
from pytz import timezone
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MotleyFoolScraper(Scraper):

    def _driver_mode(self):
        return SELENIUM

    def _login_via_selenium(self):
        driver = super()._login_via_selenium()

        # Go to the URL
        driver.get("https://www.fool.com/auth/authenticate")

        # Wait for the login form to appear, then enter the username and password
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.ID, 'usernameOrEmail'))).send_keys(self.username)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.ID, 'password'))).send_keys(self.password)

        # Click the submit button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'btn-login'))).click()

        # Wait for the page to load, then parse the HTML with BeautifulSoup
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))
        time.sleep(10)

        return driver

    def _parse(self, soup) -> PageContent:
        main = soup.find('main', {'id': 'main-content'})
        title = main.find('h3')
        title = title.get_text() if title else ''
        title = title.strip()

        date = main.find('h3').find_previous_sibling("div") if title else None
        date = date.find_all('span')[1].get_text() if date else None
        date = self._parse_date(date) if date else datetime.utcnow()

        body_text = ''
        divs = main.find_all('div', {'class': 'html-body-part'})
        for div in divs:
            paragraphs = div.find_all('p')
            for p in paragraphs:
                body_text += "\n\n" + p.get_text().strip()

        return PageContent(
            title=title,
            body=body_text.strip(),
            date=date
        )

    def _parse_date(self, date: str) -> datetime:
        dt = datetime.strptime(date, '%b %d, %Y')
        ts = timezone('UTC').localize(dt)
        return ts

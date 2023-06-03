from .scraper import Scraper, PageContent
from datetime import datetime
from pytz import timezone


class SeekingAlphaScraper(Scraper):

    def _get_payload_structure(self):
        return {
            "data": {
                "type": "loginTokens",
                "relationships": {
                    "user": {
                        "data": {
                            "email": self.username,
                            "password": self.password
                        }
                    }
                }
            }
        }

    def _get_login_url(self):
        return "https://seekingalpha.com/api/v3/login_tokens"

    def _parse(self, soup) -> PageContent:
        # container at section[data-test-id="card-container"]
        container = soup.find('section', {'data-test-id': 'card-container'})

        if container:

            date = container.find('span', {'data-test-id': 'post-date'})
            date = date.get_text() if date else ''
            date = self._parse_time(date) if date else datetime.utcnow()

            title = container.find('h1')
            title = title.get_text() if title else ''
            title = title.strip()

            body = container.find('div', {'data-test-id': 'article-content'}
                                  ).find('div', {'data-test-id': 'content-container'})
            body_text = ''
            for t in body.children:
                if t.name in ['p', 'h2']:
                    body_text += '\n\n' + t.get_text()
            body_text = body_text.strip()

            return PageContent(title=title, body=body_text, date=date)

        return PageContent(title='', body='', date=datetime.utcnow())

    def _parse_time(self, dt: str) -> datetime:
        utc = tz = timezone('UTC')
        if dt.endswith(" ET"):
            tz = timezone('US/Eastern')
            dt = dt.replace(" ET", "")

        ts = datetime.strptime(dt, '%B %d, %Y %I:%M %p')
        ts = tz.localize(ts)
        ts = ts.astimezone(utc)
        return ts

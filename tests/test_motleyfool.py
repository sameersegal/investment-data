import os
import unittest

from bs4 import BeautifulSoup
from scrapers import MotleyFoolScraper
from datetime import datetime
from pytz import timezone
from dotenv import load_dotenv
load_dotenv()

class MotleyFool(unittest.TestCase):

    def test_parsedate(self):
        scraper = MotleyFoolScraper('', '')
        dt = scraper._parse_date('Jun 1, 2023')
        self.assertEqual(dt, datetime(
            2023, 6, 1, 0, 0, tzinfo=timezone('UTC')))

    def test_scrape_page(self):
        url = "https://www.fool.com/premium/coverage/4056/coverage/2023/05/31/does-pinterest-have-10-bagger-potential/"
        expected_title = "Does Pinterest Have 10-Bagger Potential?"
        expected_body = """Pinterest (NYSE: PINS) faces some strong competition. Watch the complete show here.

Anand Chokkavelu: Maybe, maybe not for a 10 bagger, but Pinterest is one that I've long loved and it might be my biggest single position. But I have the one threat that unlike trying to sauce that as Lemon8, TikTok's other social media company or like how much traction is this getting? It's hard to tell.

Bill Mann: Which one?

Anand Chokkavelu: Lemon8.

Bill Mann: Lemon8.

Anand Chokkavelu: It's newer. The tag line is if Instagram and Pinterest had a baby.

Bill Mann: They didn't call it PInstagram?

Anand Chokkavelu: Right.

Bill Mann: Probably they gotten sued. That's fine. Take that smoke all day. Go ahead.

Anand Chokkavelu: Fundamentally, I just can't get past. The social media company doesn't get as much love. You don't get the headlines like Twitter and you're not trying to do the Metaverse and stuff, but it's just that 80 percent of US moms use it. It's the social media that's most made for monetizing. They've got the new-ish CEO coming in to help monetize it. Each quarter I'm like, oh is this the quarter and it's still quite, that quick. But you're on Pinterest to do projects and if you use it like I would use it, it's just like, hey, I'm going to build a deck. Let me see what other people have built and stuff. You can easily see like, oh, wait, here's a lumber company that says they can give me my decking a lot cheaper than Home Depot and stuff. Well, what's this? It's made for that and if they can make it easier on folks. I like their floor."""
        scraper = MotleyFoolScraper(
            os.getenv('MOTLEY_FOOL_USERNAME'), os.getenv('MOTLEY_FOOL_PASSWORD'))

        content = scraper.scrape(url)
        # print("----")
        # print(content.body)
        # print("----")
        # print(expected_body)
        # print("----")

        self.maxDiff = None
        self.assertEqual(content.title, expected_title)
        self.assertEqual(content.body, expected_body)
        utc = timezone('UTC')
        self.assertEqual(content.date, datetime(
            2023, 6, 1, 0, 0, tzinfo=utc))
        
    def test_scrape_links(self):
        url = "https://www.fool.com/premium/company/NYSE/PINS/"

        scraper = MotleyFoolScraper(
            os.getenv('MOTLEY_FOOL_USERNAME'), os.getenv('MOTLEY_FOOL_PASSWORD'))
        
        html = ''
        with open('tests/PINS.html', 'r') as f:
            html = f.read()

        # content = scraper.parse_links(html)
        soup = BeautifulSoup(html, 'html.parser')
        premium_analysis = soup.find_all('h5')
        
        for pa in premium_analysis:
            print(pa.text)
            print(pa['class'])

        if premium_analysis:
            links = premium_analysis.find_next_silbling('div').find_all('a')
            for link in links:
                print(link['href'])
        else:
            self.fail("Premium Analysis not found")

# Read links from a `links.log` file and scrape the data from the links
# Once done reading, mark the link as done in the `links.log` file
import os
from dotenv import load_dotenv
from scrapers import SeekingAlphaScraper, PageContent
load_dotenv()


def scrape(link: str) -> PageContent:
    scraper = None
    if link.startswith("https://seekingalpha.com"):
        scraper = SeekingAlphaScraper(
            os.getenv('USERNAME'), os.getenv('PASSWORD'))
    else:
        raise Exception(f'No scraper found for the link {link}')

    return scraper.scrape(link)


def main():

    links = []
    with open('PINS/links.log', 'r') as f:
        links = f.readlines()

    for link in links:
        if not '$DONE$' in link:
            print(link)
            content = scrape(link)
            print('date:', content.date)
            print('title:', content.title)
            print('body:', content.body[:150] + '...' + content.body[-50:])
            print("\n\n")

if __name__ == '__main__':
    main()

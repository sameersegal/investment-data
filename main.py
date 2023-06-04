import os
from dotenv import load_dotenv
from scrapers import PageContent, SeekingAlphaScraper, MotleyFoolScraper
load_dotenv()


def scrape(link: str) -> PageContent:
    scraper = None
    if link.startswith("https://seekingalpha.com"):
        scraper = SeekingAlphaScraper(
            os.getenv('SEEKING_ALPHA_USERNAME'), os.getenv('SEEKING_ALPHA_PASSWORD'))
    elif link.startswith("https://www.fool.com"):
        scraper = MotleyFoolScraper(
            os.getenv('MOTLEY_FOOL_USERNAME'), os.getenv('MOTLEY_FOOL_PASSWORD'))
    else:
        raise Exception(f'No scraper found for the link {link}')

    return scraper.scrape(link)


def main():

    links = []
    with open('links.log', 'r') as f:
        links = f.readlines()

    for link in links:
        if not '$DONE$' in link:
            print(link)
            content = scrape(link)
            print('date:', content.date)
            print('title:', content.title)
            print('body:', content.body)
            # print('body:', content.body[:150] + '...' + content.body[-50:])
            print("\n\n")


if __name__ == '__main__':
    main()

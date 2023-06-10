import os
from urllib.parse import urlparse
from dotenv import load_dotenv
from scrapers import PageContent, Scraper, SeekingAlphaScraper, MotleyFoolScraper, IOFundScraper
import weakref
import yaml
import hashlib
load_dotenv()

OUTPUT_DIRECTORY = os.path.join(os.getcwd(), 'output')


def get_domain(link: str) -> str:
    domain = urlparse(link).hostname
    parts = domain.split('.')
    if len(parts) > 2:
        domain = '.'.join(parts[-2:])
    return domain


# _scrapers = weakref.WeakValueDictionary()
_scrapers = {}


def get_scraper(link: str) -> Scraper:
    domain = get_domain(link)
    if domain in _scrapers:
        return _scrapers[domain]

    scraper = None
    if domain == 'seekingalpha.com':
        scraper = SeekingAlphaScraper(
            os.getenv('SEEKING_ALPHA_USERNAME'), os.getenv('SEEKING_ALPHA_PASSWORD'))
    elif domain == 'fool.com':
        scraper = MotleyFoolScraper(
            os.getenv('MOTLEY_FOOL_USERNAME'), os.getenv('MOTLEY_FOOL_PASSWORD'))
    elif domain == 'io-fund.com':
        scraper = IOFundScraper(
            os.getenv('IO_FUND_USERNAME'), os.getenv('IO_FUND_PASSWORD'))
    else:
        raise Exception(f'No scraper found for the link {link}')
    _scrapers[domain] = scraper

    return _scrapers[domain]


def scrape(link: str) -> PageContent:
    scraper = get_scraper(link)
    return scraper.scrape(link)


def main():

    links = []
    with open('links.log', 'r') as f:
        links = f.readlines()

    pending_links = [link.strip() for link in links if not "$DONE$" in link]

    pending_links.sort(key=lambda x: get_domain(x))

    print(f"Processing {len(pending_links)} out of {len(links)}")

    for link in pending_links:
        print(link)
        content = scrape(link)

        # generate hash from link

        hash = generate_hash(link) + '.yml'
        output_file = os.path.join(OUTPUT_DIRECTORY, hash)
        with open(output_file, 'w') as f:
            data = {
                'url': link,
                'date': content.date,
                'title': content.title,
                'body': content.body
            }
            yaml.dump(data, f, sort_keys=False)
            # f.write(yaml_data)
            # print(yaml_data)
            # print("\n\n")


def generate_hash(link: str) -> str:
    hash_object = hashlib.sha256(link.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig


if __name__ == '__main__':
    main()

# Investment Data

This repository contains a few webscrapers to capture data from trusted financial sources to build a local personal knowledge base. These websites require paid subscriptions and valid credentials.

## Setup

2. Copy env.template to .env and populate it with valid credentials. Example:
```
SEEKING_ALPHA_USERNAME=
SEEKING_ALPHA_PASSWORD=
MOTLEY_FOOL_USERNAME=
MOTLEY_FOOL_PASSWORD=
```
3. Poetry setup
```
$poetry shell
$poetry install
```
1. Create a `links.log` file with urls.
4. Run
```
$poetry run python3 main.py
```
5. Unit Testing
```
$poetry run python3 -m unittest test/test_*

# To run only a specific test
$poetry run python3 -m unittest test.test_seekingalpha.SeekingAlpha.test_url1
```
6. Instructions for Milvus (Vector Database)

[https://milvus.io/docs/install_standalone-docker.md](https://milvus.io/docs/install_standalone-docker.md)

### Todos

- [ ] Generate links to scrape by going to search page and typing stock code
- [X] Maintain session across multiple links to avoid the overhead of login
- [X] Write content to local file system

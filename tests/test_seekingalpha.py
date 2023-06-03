import os
import unittest
from scrapers.seekingalpha import SeekingAlphaScraper
from datetime import datetime
from pytz import timezone


class SeekingAlpha(unittest.TestCase):

    def test_timeparsing(self):
        scraper = SeekingAlphaScraper('', '')
        utc = timezone('UTC')

        date = 'May 31, 2023 6:20 AM ET'
        date = scraper._parse_time(date)
        self.assertEqual(date, datetime(
            2023, 5, 31, 10, 20, tzinfo=utc))

    def test_url1(self):
        url = "https://seekingalpha.com/article/4608422-pinterest-brace-for-weakness?utm_campaign=%7Clogin_now_link&utm_medium=email&utm_source=seeking_alpha"
        expected_title = "Pinterest: Brace For Weakness"
        expected_body = """Spencer Platt

Investment thesis

Pinterest (NYSE:PINS) stock has been one of the hottest during the COVID-era stock market frenzy of 2021. Since then, the stock price declined more than three-fold, and some investors might consider the stock to be oversold and undervalued. But my analysis reveals that the company is still very generously valued even after a massive selloff. Moreover, the company is facing near-term headwinds and is far from generating sustainable free cash flows.

Company information

Pinterest is a social media platform for visual discovery. The platform allows contributors to share graphical images, as well as save and organize ideas and recommendations into collections. Since its launch in 2010, Pinterest has expanded its community beyond 350 million active users. It allows the company to generate revenue by delivering ads on the platform, which is represented by the website and mobile application. Pinterest went public four years ago at $19 per share.

The company's fiscal year ends December 31, and it operates as a single segment. Pinterest generates revenue across the world, but North America represents a vast 80% of total sales.

Pinterest's latest 10-K report

Financials

Pinterest went public relatively recently, so we do not have an opportunity to analyze the company's financials over the past decade as I usually do. On the other hand, six-years horizon is not that bad since we have financial performance available since FY2017.

Author's calculations

The company delivered a stellar 30% revenue CAGR over the last six years, with margins expanding notably. Operating margin and free cash flow [FCF] margins were mostly positive during the last two years. Please note that for FCF, I deduct stock-based compensation [SBC] since it is a non-cash item, though it has been significant in recent years.

Apart from the positive signs mentioned in the above paragraph, let me emphasize your attention to the challenges the company faces in the harsh macro environment. Let me now zoom in and look at the recent several quarters' dynamics.

Seeking Alpha

As you can see from the above table, the topline growth pace decelerated dramatically. The company demonstrated solid double-digit revenue growth, but in the last four quarters in a row, it has been much lower, with the two latest quarters growing slower than a 5% rate. What is also bad for the company is that expenses are growing much faster than the topline meaning that the business profitability has been deteriorating rapidly.

Seeking Alpha

From the cash flow viewpoint, you can see that the operating cash flow has been deteriorating YoY massively during the last three quarters in a row. These dynamics of recent quarters look very alarming to me since the management seems to lag behind the rapidly changing adverse macro environment. The management's decision to lay off 150 employees looks late and insufficient. I think so because 150 employees represent 5% of the headcount, while other technology companies cutting the workforce by a double-digit percentage. On the other hand, the company's balance sheet looks very healthy, with a confident net cash position and fortress liquidity ratios.

Seeking Alpha

The company might be cautious in laying off employees in order not to lose their brightest engineers, but I consider this a risky bet by the management. Even companies with vast resources like Amazon (AMZN) and Google (GOOG) implement significant cost-cutting initiatives and smaller players like Pinterest should do so as well.

Valuation

I use discounted cash flow [DCF] approach for Pinterest valuation. The company does not pay dividends and is a growth company, so DCF looks reasonable. For the discount rate, I prefer 10%, which is within the WACC range suggested by valueinvesting.io. Revenue is expected to compound at about 8% CAGR, according to earnings consensus estimates. Pinterest has not reached sustainable FCF yet, but the latest quarter demonstrated a solid 5% margin ex-SBC. On the other hand, on the TTM basis, the FCF margin is still negative. Given near-term challenges, I estimate that in 2023 the company is not likely to sustain Q1 FCF metrics, and the average for the year will be at 2%. Consensus estimates project EPS to grow double digits each year, so I expect the FCF margin to expand by at least two percentage points early.

Author's calculations

As you can see from the above table, the fair business value is about $16 billion under the assumptions I described earlier in this article. The current market cap is about half a billion higher, meaning the stock is slightly overvalued.

To cross-check my DCF analysis, I would also like to examine the valuation multiples. According to Seeking Alpha Quant ratings, PINS has a relatively low grade of "D-". Valuation ratios are multiple times higher compared to median sector values.

Seeking Alpha

Pinterest bulls might argue that comparison to the sector would be inappropriate since the company has grown aggressively and deserves to trade at a premium. To add context to Pinterest's high valuation multiples, in my opinion, I would like to demonstrate the following table.

Compiled by the author based on Seeking Alpha's data

As you can see, Pinterest is traded at a forward P/S ratio which is higher than Meta's (META). According to consensus earnings estimates, the revenue growth profile of Pinterest looks slightly better for the next decade, but the company is very far from Meta's profitability. Meta is much better at converting sales to operating cash flows and it will take PINS several years to match Meta's profitability. I believe the slightly positive gap for Pinterest in terms of projected revenue growth does not outweigh the large gap in profitability. Therefore, given this context, I believe that Pinterest is too generously valued, which backs my DCF analysis.

Risks to consider

From the operating perspective, I consider Pinterest's significant risk to be maintaining its thriving ecosystem of contributors and advertisers. Fierce competition in attracting and retaining advertisers could affect the platform's long-term success. The company needs to balance user experience and advertising as well as adapt to changing user preferences, which is challenging. Failing to find this balance poses significant threats to Pinterest's growth prospects, which are priced in the current market capitalization.

As a social media, Pinterest stores vast amounts of personal data of all the participants on the platform. Any potential misuse of user data or cyber breaches will significantly hit the company's reputation and public image. Apart from reputational risks, the company might face litigations from users or advertisers, which can lead to unexpected and significant cash outflows in the form of fines and penalties.

Last but not least, Pinterest is heavily dependent on the advertisers' marketing budgets, which are vulnerable to overall economic health. In current harsh circumstances, businesses' marketing budgets will likely be optimized, meaning temporary shrinkage of the company's addressable market.

Bottom line

Overall, I would neither buy PINS nor recommend doing it at current levels. The current stock price is not attractive, as my valuation analysis suggests. Moreover, the company's revenue growth pace decelerated massively compared to 2021, with margins shrinking. Given the underlying fundamentals, I expect the stock price to decline, so I assign it a "Sell" rating."""
        scraper = SeekingAlphaScraper(
            os.getenv("SEEKING_ALPHA_USERNAME"),
            os.getenv("SEEKING_ALPHA_PASSWORD")
        )
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
            2023, 5, 31, 10, 20, tzinfo=utc))

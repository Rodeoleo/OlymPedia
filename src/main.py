from MedalScraper import MedalScraper
from datetime import datetime

START_DATE = datetime(2024, 7, 26) # Opening Ceremony day
today_date = datetime.now()

medal_url = "https://en.wikipedia.org/wiki/2024_Summer_Olympics_medal_table"
medal_scraper = MedalScraper(medal_url)



day_counter = (today_date - START_DATE).days
medal_scraper.scrape(day_counter)

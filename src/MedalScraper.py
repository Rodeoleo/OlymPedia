from OlympicsScraper import OlympicsScraper
import os
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

class MedalScraper(OlympicsScraper):
    def __init__(self, url):
        super().__init__(url)

    def scrape(self):
        pass

    def parse(self):
        pass

    def update_gold(self):
        pass

    def scrape_silver(self):
        pass 

    def scrape_table(self, day_counter):
        response = requests.get(self.url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table', {'class': "wikitable sortable notheme plainrowheaders jquery-tablesorter"})
        
        rows = []
        for tr in table.find_all('tr')[1:-1]:  # Skip the header row and last row
            cells = tr.find_all('td')
            country_name = tr.find('a').text
            row = [int(cell.get_text(strip=True)) for cell in cells]
            if len(row) == 5:
                row.pop(0)
            rows.append([country_name] + row)

        header = ["country", "gold", "silver", "bronze", "total"]

        today_medal_table = pd.DataFrame(rows, columns=header)
        
        if os.path.exists('./data/medal_table.json'):
            try:
                with open('./data/medal_table.json') as file:
                    df_dict = json.load(file)
            except json.JSONDecodeError:
                df_dict = {}
        else: # new dict
            df_dict = {}

        df_dict[int(day_counter)] = today_medal_table.to_dict(orient='records')

        with open('./data/medal_table.json', 'w') as file:
            json.dump(df_dict, file, indent=4)

        df_file_path = f"./data/medal_table_day{day_counter}.csv"
        today_medal_table.to_csv(df_file_path, index=False)

    
    def save_file(self):
        pass
from OlympicsScraper import OlympicsScraper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

class MedalScraper(OlympicsScraper):
    def __init__(self, url):
        super().__init__(url)
        self.top10_gold = []
        self.top10_silver = []
        self.top10_bronze = []
        self.top10_total = []

    def scrape(self, day_counter):
        self._update_top10_bronze()
        self._update_top10_silver()
        self._update_top10_gold()
        self._update_top10_total()
        self.scrape_table(day_counter)

    def parse(self):
        pass

    def _extract_top10(self, sel_table):
        row_elements = sel_table.find_elements(By.XPATH, './/tbody/tr')

        top10 = []
        for row in row_elements[:10]:
            cell = row.find_elements(By.XPATH, './th/a')
            country = cell[0].text.strip()
            top10.append(country)

        return top10
    
    def _update_top10(self, column_index, top10_list_name):
        self.driver.get(self.url)
        sorter_xpath = f'//*[@id="mw-content-text"]/div[1]/table[3]/thead/tr/th[{column_index}]'
        sorter = WebDriverWait(self.driver, 2).until(
            EC.presence_of_element_located((By.XPATH, sorter_xpath))
        )
        
        while sorter.get_attribute("class") != "headerSort headerSortDown":
            sorter.click()
            time.sleep(0.1)
        
        table_xpath = '//*[@id="mw-content-text"]/div[1]/table[3]'
        table = self.driver.find_element(By.XPATH, table_xpath)
        top10_list = self._extract_top10(table)
        setattr(self, top10_list_name, top10_list)
        time.sleep(1)

    def _update_top10_gold(self):
        self._update_top10(3, 'top10_gold')

    def _update_top10_silver(self):
        self._update_top10(4, 'top10_silver')

    def _update_top10_bronze(self):
        self._update_top10(5, 'top10_bronze')

    def _update_top10_total(self):
        self._update_top10(6, 'top10_total')

    def scrape_table(self, day_counter): #Using bs4
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
        
        self._save_file_medal_table(today_medal_table, day_counter)

    
    def _save_file_medal_table(self, df, day_counter):
        if os.path.exists('./data/medal_table.json'):
            try:
                with open('./data/medal_table.json') as file:
                    df_dict = json.load(file)
            except json.JSONDecodeError:
                df_dict = {}
        else: # new dict
            df_dict = {}

        df_dict[int(day_counter)] = df.to_dict(orient='records')

        with open('./data/medal_table.json', 'w') as file:
            json.dump(df_dict, file, indent=4)

        df_file_path = f"./data/medal_table_by_day/medal_table_day{day_counter}.csv"
        df.to_csv(df_file_path, index=False)
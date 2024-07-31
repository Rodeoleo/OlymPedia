from selenium import webdriver
from abc import ABC, abstractmethod
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
import time

class OlympicsScraper(ABC):
    def __init__(self, url):
        self.url = url
        self.driver = self._setup_driver()
    
    def _setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

    @abstractmethod
    def scrape(self):
        pass

    @abstractmethod
    def parse(self):
        pass

    def save_table(self, df, filepath):
        df.to_csv(filepath, index=False)
    

    
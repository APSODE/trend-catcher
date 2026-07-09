from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.crawler_api.service.url_extractor.BaseUrlFetcher import BaseUrlFetcher


class SeleniumURLFetcher(BaseUrlFetcher):

    async def fetch(self, url: str) -> str:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)
        try:
            driver.get(url)
            if driver.status_code != 200:
            return driver.page_source



import random
import time

from httpcore import TimeoutException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.crawler_api.exception.not_found_exception import NotFoundException
from src.crawler_api.service.url_fetcher.base_url_fetcher import BaseUrlFetcher
from src.crawler_api.util.check_robots import CheckRobots


class SeleniumURLFetcher(BaseUrlFetcher):

    async def fetch(self, url: str) -> str | None:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        robots = CheckRobots(url)
        await robots.load()

        driver = webdriver.Chrome(options=options)
        try:
            if not await robots.is_allowed(url):
                return None
            driver.get(url)
            return driver.page_source
        except TimeoutException:
            raise NotFoundException()
        except Exception as e:
            raise NotFoundException(e.__str__())


    async def fetch_by_all(self, urls: list[str], base_url : str) -> list[str]:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)

        robots = CheckRobots(base_url)
        await robots.load()
        results = []
        for url in urls:
            try:
                if not await robots.is_allowed(url):
                    results.append("")
                driver.get(url)
                results.append(driver.page_source)
                time.sleep(random.uniform(1.5, 3.5))

            except TimeoutException:
                results.append("")
        return results


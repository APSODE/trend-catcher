import asyncio
import logging
import random
import time

from selenium import webdriver
from selenium.common import WebDriverException, TimeoutException
from selenium.webdriver.chrome.options import Options

from src.crawler_api.exception.not_found_exception import NotFoundException
from src.crawler_api.service.url_fetcher.base_url_fetcher import BaseUrlFetcher
from src.crawler_api.util.check_robots import CheckRobots


logger = logging.getLogger(__name__)

SELENIUM_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")

class SeleniumURLFetcher(BaseUrlFetcher):
    def __init__(self):
        self._driver : webdriver.Chrome | None = None

    def __get_driver(self) -> webdriver.Chrome:
        driver = self._driver
        if driver is None:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument(f"user-agent={SELENIUM_USER_AGENT}")
            driver = webdriver.Chrome(options=options)
            self._driver = driver

        return driver

    def close(self):
        if self._driver is not None:
            self._driver.quit()
            self._driver = None

    def __del__(self):
        self.close()

    @staticmethod
    def __load_page(driver: webdriver.Chrome, url: str) -> str:
        driver.get(url)
        return driver.page_source

    @staticmethod
    def __load_page_with_delay(driver: webdriver.Chrome, url: str) -> str:
        driver.get(url)
        page_source = driver.page_source
        time.sleep(random.uniform(1.5, 3.5))
        return page_source

    async def fetch(self, url: str) -> str | None:

        robots = CheckRobots(url)
        await robots.load()

        driver = self.__get_driver()

        try:
            if not await robots.is_allowed(url):
                return None

            return await asyncio.to_thread(self.__load_page, driver, url)

        except TimeoutException:
            raise NotFoundException()

        except WebDriverException as e:
            raise NotFoundException(str(e)) from e


    async def fetch_by_all(self, urls: list[str], base_url: str) -> list[str]:

        driver = self.__get_driver()

        robots = CheckRobots(base_url)
        await robots.load()

        results : list[str] = []

        for url in urls:
            try:
                if not await robots.is_allowed(url):
                    results.append("")
                    continue

                page_source = await asyncio.to_thread(self.__load_page_with_delay, driver, url)
                results.append(page_source)

            except TimeoutException:
                results.append("")

            except WebDriverException as e:
                logger.exception("selenium fetch_all error occurred : %s", e)
                results.append("")

        return results


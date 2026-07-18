import urllib.robotparser
from urllib.parse import urlparse, urljoin

import httpx


class CheckRobots:
    def __init__(self, url: str):
        parse_url = urlparse(url)

        self.__base_url = f"{parse_url.scheme}://{parse_url.netloc}"
        self.__robots_url = f"{self.__base_url}/robots.txt"
        self.__rp = urllib.robotparser.RobotFileParser()

    async def load(self):
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(self.__robots_url)

                if response.status_code != 200:
                    self.__is_loaded = False
                    return

                self.__rp.parse(
                    response.text.splitlines()
                )

                self.__is_loaded = True

        except Exception:
            self.__is_loaded = False


    async def is_allowed(self, url : str) -> bool:
        if not self.__is_loaded:
            return True
        url = urljoin(self.__base_url, url)
        return self.__rp.can_fetch(useragent="*", url=url)






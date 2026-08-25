import logging
import urllib.robotparser
import httpx

from urllib.parse import urlparse, urljoin

from src.crawler_api.util.header_provider import get_httpx_header


logger = logging.getLogger(__name__)

headers = get_httpx_header()

class CheckRobots:
    def __init__(self, url: str):
        parse_url = urlparse(url)

        self._base_url = f"{parse_url.scheme}://{parse_url.netloc}"
        self._robots_url = f"{self._base_url}/robots.txt"
        self._rp = urllib.robotparser.RobotFileParser()
        self._is_loaded = False

    async def load(self):
        try:
            async with httpx.AsyncClient(headers=headers, timeout=5.0) as client:
                response = await client.get(self._robots_url)

                if response.status_code != 200:
                    logger.warning("robot.txt does not exist: %s", self._robots_url)
                    self._is_loaded = False
                    return

                self._rp.parse(response.text.splitlines())
                self._is_loaded = True
        except (httpx.ConnectTimeout, httpx.TimeoutException) as e:
            logger.warning("robots.txt connection time error : %s", e)
            self._is_loaded = False

        except Exception as e:

            logger.exception("robot.txt setting error occurred: %s",e)
            self._is_loaded = False
            return

    async def is_allowed(self, url: str) -> bool:
        if not self._is_loaded:
            return True
        url = urljoin(self._base_url, url)
        return self._rp.can_fetch(useragent="*", url=url)






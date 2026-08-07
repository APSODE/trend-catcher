import logging
import urllib.robotparser
import httpx

from urllib.parse import urlparse, urljoin


logger = logging.getLogger(__name__)
class CheckRobots:
    def __init__(self, url: str):
        parse_url = urlparse(url)

        self._base_url = f"{parse_url.scheme}://{parse_url.netloc}"
        self._robots_url = f"{self._base_url}/robots.txt"
        self._rp = urllib.robotparser.RobotFileParser()
        self._is_loaded = False

    async def load(self):
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(self._robots_url)

                if response.status_code != 200:
                    self._is_loaded = False
                    return

                self._rp.parse(response.text.splitlines())
                self._is_loaded = True

        except Exception as e:

            logger.exception("robot.txt 설정 오류 발생 : %s",e)
            self._is_loaded = False
            return

    async def is_allowed(self, url: str) -> bool:
        if not self._is_loaded:
            return True
        url = urljoin(self._base_url, url)
        return self._rp.can_fetch(useragent="*", url=url)






import urllib.robotparser
from urllib.parse import urlparse, urljoin


class CheckRobots:
    def __init__(self, url: str):
        parse_url = urlparse(url)

        self.__base_url = f"{parse_url.scheme}://{parse_url.netloc}"
        robots_url = f"{self.__base_url}/robots.txt"
        self.__rp = urllib.robotparser.RobotFileParser()
        self.__rp.set_url(robots_url)

        try:
            self.__rp.read()
            self.__is_loaded = True
        except Exception as e:
            self.__is_loaded = False


    async def is_allowed(self, url : str) -> bool:
        if not self.__is_loaded:
            return True
        url = urljoin(self.__base_url, url)
        return self.__rp.can_fetch(user_agent="*", url=url)






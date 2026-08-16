from tenacity import retry, wait_random, stop_never, stop_after_attempt
from urllib.parse import quote
import requests
from duckduckgo_search import DDGS


class Crawler:
    def __init__(self):
        pass

    @staticmethod
    @retry(wait=wait_random(min=3, max=8), stop=stop_never)
    def bing(keywords):
        response = requests.get(
            f"https://cn.bing.com/search?format=rss&q={quote(f'{keywords}')}", timeout=5
        )
        content = response.text
        if len(content) < 1000:
            raise Exception("无效的RSS响应")

        return content

    @staticmethod
    @retry(wait=wait_random(min=20, max=30), stop=stop_never)
    def duckduckgo(keyword, proxy):
        ddgs = DDGS(proxy=proxy)
        results = ddgs.text(keywords=keyword, max_results=50)
        return str(results)

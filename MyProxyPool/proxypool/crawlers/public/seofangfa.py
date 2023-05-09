from proxypool.crawlers.base import BaseCrawler
from parsel import Selector


BASE_URL = 'https://proxy.seofangfa.com/'


class SeofangfaCrawler(BaseCrawler):
    """
    seofangfa：https://proxy.seofangfa.com/
    """
    urls = [BASE_URL]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }

    def parse(self, html):
        selector = Selector(text=html)
        for tr in selector.css('.table tbody tr'):
            ip = tr.css('td')[0].get()
            ip = ip.replace('<td>','').replace('</td>','')
            port = tr.css('td')[1].get()
            port = port.replace('<td>', '').replace('</td>', '')
            proxy = ip + ':' + port
            yield proxy

from lxml import html
etree = html.etree
from proxypool.crawlers.base import BaseCrawler


MAX_PAGE = 5
BASE_URL = 'https://www.kuaidaili.com/free/{type}/{page}/'


class KuaidailiCrawler(BaseCrawler):
    """
    快代理：https://www.kuaidaili.com
    """
    urls = [BASE_URL.format(type=type,page=page) for type in ['inha'] for page in range(1, MAX_PAGE+1)] # inha：国内高匿代理
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }

    def parse(self, html):
        html = etree.HTML(html)
        for tr in html.xpath('//*[@id="list"]/table/tbody/tr'):
            ip = tr.xpath('./td[1]/text()')[0]
            port = tr.xpath('./td[2]/text()')[0]
            proxy = ip + ':' + port
            yield proxy

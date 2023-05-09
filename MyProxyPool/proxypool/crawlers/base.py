from retrying import RetryError, retry
import requests
from loguru import logger
import time
from proxypool.utils.setting import GET_TIMEOUT


class BaseCrawler(object):
    # stop_max_attempt_number：在停止之前尝试的最大次数，默认5次，最后一次如果还是有异常则会抛出异常，停止运行
    # retry_on_result：如果指定的函数返回True，则重试，否则抛出异常退出；x表示函数的返回值
    # wait_fixed：两次retrying之间停留时长，毫秒
    @retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is None, wait_fixed=2000)
    def fetch(self, url, **kwargs):
        """
        获取网页内容
        """
        try:
            kwargs.setdefault('timeout', GET_TIMEOUT) # 设置超时时间，若超时未响应，则抛出异常
            kwargs.setdefault('verify', False) # 关闭SSL证书验证
            kwargs.setdefault('headers', self.headers)
            response = requests.get(url, **kwargs)
            if response.status_code == 200:
                response.encoding = 'utf-8'
                return response.text
        except (requests.ConnectionError, requests.ReadTimeout):
            return

    def process(self, html, url):
        """
        解析网页
        """
        for proxy in self.parse(html):
            logger.info(f'fetched proxy {proxy} from {url}')
            yield proxy

    def crawl(self):
        """
        爬取proxy主要实现逻辑
        """
        for url in self.urls:
            try:
                logger.info(f'fetching {url}')
                html = self.fetch(url)
                if not html:
                    continue
                time.sleep(.5)
                yield from self.process(html, url) # 这里不能用yield
            except RetryError:
                logger.error(
                    f'crawler {self} crawled proxy unsuccessfully, '
                    'please check if target url is valid or network issue')


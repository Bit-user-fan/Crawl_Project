from proxypool.crawlers.public.kuaidaili import KuaidailiCrawler
from proxypool.crawlers.public.seofangfa import SeofangfaCrawler
import json
from loguru import logger


class Getter(object):
    crawl_list = [KuaidailiCrawler(), SeofangfaCrawler()]
    def run(self):
        proxydict = {}
        for Crawler in self.crawl_list:
            for proxy in Crawler.crawl():
                proxydict.update({proxy:5}) # 初始分数设置为5

        with open('../storages/proxydict.json', encoding='utf-8',mode='w') as fp:
            fp.write(json.dumps(proxydict))

        num = len(proxydict)
        logger.info(f'Co_save proxies: {num}')

if __name__ == '__main__':
    getter = Getter()
    getter.run()
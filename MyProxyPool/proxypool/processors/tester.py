import json
from loguru import logger
import asyncio
import aiohttp
from proxypool.utils.setting import TEST_TIMEOUT, TEST_URL, TEST_VALID_STATUS, CONCURRENCY


class Tester(object):
    proxydict = None
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }

    semaphore = asyncio.Semaphore(CONCURRENCY)

    def __init__(self):
        self.loop = asyncio.get_event_loop()

    async def test(self, proxy):
        if self.proxydict[proxy] == 0: # 若代理分数为0，从代理池中剔除
            self.proxydict.pop(proxy)
            return
        async with self.semaphore:
            logger.info(f'testing: proxy: {proxy}, score: {self.proxydict[proxy]}')
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(TEST_URL, proxy=f'http://{proxy}', timeout=TEST_TIMEOUT) as response:
                        if response.status in TEST_VALID_STATUS: # 测试有效即设置分数为100
                            self.proxydict[proxy] = 100
                        else:
                            self.proxydict[proxy] -= 1 # 没有得到有效状态码即将分数减1
                except:
                    self.proxydict[proxy] -= 1 # 测试无效即将分数减1
            logger.info(f'after testing: proxy: {proxy}, score: {self.proxydict[proxy]}')


    def run(self):
        with open('../storages/proxydict.json', encoding='utf-8', mode='r') as fp:
            self.proxydict = json.loads(fp.read())
        count = len(self.proxydict)
        logger.debug(f'{count} proxies to test')
        tasks = [asyncio.ensure_future(self.test(proxy)) for proxy in self.proxydict.keys()]
        self.loop.run_until_complete(asyncio.wait(tasks))
        # 测试后，更新代理池
        with open('../storages/proxydict.json', encoding='utf-8', mode='w') as fp:
            fp.write(json.dumps(self.proxydict))

if __name__ == '__main__':
    tester = Tester()
    tester.run()
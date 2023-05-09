from loguru import logger
from proxypool.processors.tester import Tester
from proxypool.processors.getter import Getter
from proxypool.processors.server import app
import time
import multiprocessing
from proxypool.utils.setting import ENABLE_TESTER, ENABLE_GETTER, ENABLE_SERVER, CYCLE_TESTER, CYCLE_GETTER


getter_process, tester_process, server_process = None, None, None

class Scheduler():
    def run_getter(self, cycle=CYCLE_GETTER):
        if not ENABLE_GETTER:
            logger.info('getter not enabled, exit')
            return
        getter = Getter()
        loop = 1
        while True:
            time.sleep(cycle) # 进入休眠
            logger.debug(f'getter loop {loop} start...')
            getter.run()
            loop += 1

    def run_tester(self, cycle=CYCLE_TESTER):
        if not ENABLE_TESTER:
            logger.info('tester not enabled, exit')
            return
        tester = Tester()
        loop = 1
        while True:
            logger.debug(f'tester loop {loop} start...')
            tester.run()
            loop += 1
            time.sleep(cycle)

    def run_server(self):
        if not ENABLE_SERVER:
            logger.info('server not enabled, exit')
            return
        app.run()

    def run(self):
        """
        分别为getter,tester,server分配一个进程，彼此并行执行，互不干扰
        """
        global getter_process, tester_process, server_process
        getter = Getter()
        getter.run() # 启动即运行，先获取代理
        try:
            logger.info('starting proxypool...')
            if ENABLE_GETTER:
                getter_process = multiprocessing.Process(target=self.run_getter)
                logger.info(f'starting getter...')
                getter_process.start()
            if ENABLE_TESTER:
                tester_process = multiprocessing.Process(target=self.run_tester)
                logger.info(f'starting tester...')
                tester_process.start()
            if ENABLE_SERVER:
                server_process = multiprocessing.Process(target=self.run_server())
                logger.info(f'starting server...')
                server_process.start()
            getter_process.join()
            tester_process.join()
            server_process.join()
        except:
            logger.info('received keyboard interrupt signal')
            getter_process.terminate()
            tester_process.terminate()
            server_process.terminate()


if __name__ == '__main__':
    scheler = Scheduler()
    scheler.run()

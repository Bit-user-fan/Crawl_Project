# base.py:获取代理时的超时时间，若超时未响应，则抛出异常
GET_TIMEOUT = 5

# tester.py:测试代理时的超时时间，若超时未响应，则抛出异常
TEST_TIMEOUT = 10
# tester.py:测试代理可用性的URL地址
TEST_URL = 'https://www.baidu.com/'
# tester.py:测试代理可用性的响应状态码列表
TEST_VALID_STATUS = [200]
# tester.py:测试代理时设置爬取的并发量
CONCURRENCY = 5

# scheduler.py:分别表示测试模块，获取模块，接口模块的开关，Ture表示开启
ENABLE_TESTER = True
ENABLE_GETTER = True
ENABLE_SERVER = True
# scheduler.py:分别表示测试模块调度，获取模块调度的休眠时间
CYCLE_TESTER = 50
CYCLE_GETTER = 300
# MyProxyPool

简易高效的代理池，提供如下功能：

定时抓取免费代理网站，对代理进行本地存储。
定时测试和筛选，剔除不可用代理，留下可用代理。
提供代理 API，随机取用测试通过的可用代理。



运行代理池：

python3 run.py

运行之后会启动 Tester、Getter、Server，这时访问 http://localhost:5000/random 即可获取一个随机可用代理。demo.py的示例展示了获取代理并爬取网页的过程。



可配置项：

开关
ENABLE_TESTER：允许 Tester 启动，默认 true
ENABLE_GETTER：允许 Getter 启动，默认 true
ENABLE_SERVER：运行 Server 启动，默认 true


CYCLE_TESTER：Tester 运行周期，即间隔多久运行一次测试，默认 50 秒

CYCLE_GETTER：Getter 运行周期，即间隔多久运行一次代理获取，默认 300 秒

TEST_URL：测试 URL，默认百度https://www.baidu.com/

GET_TIMEOUT：获取代理超时时间，默认5秒

TEST_TIMEOUT：测试超时时间，默认 10 秒

TEST_VALID_STATUS：测试有效的状态码

CONCURRENCY：测试代理时设置爬取的并发量，默认值5



扩展代理爬虫：

代理的爬虫均放置在 proxypool/crawlers/public 文件夹下，目前对接了2个代理的爬虫。

若需要扩展爬虫，只需在 public 文件夹下新建一个 Python 文件声明一个 Class ，将Class加入processors/getter文件的crawl_list即可。



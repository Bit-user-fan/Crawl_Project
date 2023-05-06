from scrapy.http import HtmlResponse
import time


class WangyinewsDownloaderMiddleware:

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        bro = spider.bro
        if request.url in spider.plate_urls:
            bro.get(request.url)
            time.sleep(2)
            # 这里可以将鼠标拖至底部，加载出更多数据
            page = bro.page_source
            return HtmlResponse(request.url, body=page, encoding='utf-8', request=request)
        else:
            return response


    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        pass

    def spider_closed(self,spider):
        pass


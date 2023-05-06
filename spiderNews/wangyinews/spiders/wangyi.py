import scrapy
from selenium import webdriver
from wangyinews.items import WangyinewsItem

class WangyiSpider(scrapy.Spider):
    name = "wangyi"
    # allowed_domains = ["www.c.c"]
    start_urls = ["https://news.163.com/"]
    plate_urls = []
    def __init__(self):
        self.bro = webdriver.Chrome(executable_path = 'D:\code\python_Crawl\spiderJob\chromedriver.exe')

    def parse(self, response):
        li_list = response.xpath('//*[@id="index2016_wrap"]/div[3]/div[2]/div[2]/div[2]/div/ul/li')
        # 解析板块内容
        for i in [1,2,4,5]:
            plate_url = li_list[i].xpath('./a/@href').extract_first()
            self.plate_urls.append(plate_url)
            yield scrapy.Request(plate_url, callback=self.parse_plate)
    # 解析板块
    def parse_plate(self, response):
        div_list = response.xpath('/html/body/div/div[3]/div[3]/div[1]/div[1]/div/ul/li/div/div[contains(@class,"data_row")]') # [contains(@class,"data_row")]剔除广告
        for div in div_list:
            detail_url = div.xpath('./div/div[1]/h3/a/@href').extract_first()
            # 剔除内容为视频的新闻
            if detail_url.split('/')[-2] == "article":
                item = WangyinewsItem()
                title = div.xpath('./div/div[1]/h3/a/text()').extract_first()
                item['title'] = title
                yield scrapy.Request(detail_url, callback=self.parse_detail, meta={'item':item})

    def parse_detail(self, response):
        item = response.meta['item']
        content = response.xpath('//*[@id="content"]/div[2]/p//text()').extract()
        content = ''.join(content)
        item['content'] = content
        yield item

    def closed(self, spider):
        self.bro.quit()
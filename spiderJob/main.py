import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from urllib.parse import urlencode
from lxml import html
import random
import pymysql
etree = html.etree


BOSS_LIST = []
LAGOU_LIST = []

chrome = webdriver.Chrome()


# 解析boss列表页数据
def parse_boss(html):
    root = etree.HTML(html)
    lis = root.xpath('//div[@class="search-job-result"]/ul/li')  # 获取列表页
    # 遍历列表页中每一条数据，进行信息提取
    for li in lis:
        title = li.xpath('div[1]/a/div[1]/span[@class="job-name"]/text()')
        position = li.xpath('div[1]//span[@class="job-area"]/text()')
        salary = li.xpath('div[1]/a/div[2]/span[@class="salary"]/text()')
        experience_education = li.xpath('div[1]/a/div[2]/ul/li/text()')
        company = li.xpath('div[1]/div/div[2]/h3/a/text()')
        # 对工作经验和学历的返回数据进行特殊处理
        extra = ""
        if len(experience_education) == 3:
            # extra = experience_education[0] # 这个字段描述的是按天计薪时，每周工作的天数：4天/周
            experience = experience_education[1]
            education = experience_education[2]
        else:
            experience = experience_education[0]
            education = experience_education[1]

        if title != []:
            print(title[0], position[0], salary[0], experience, education, company[0])
            BOSS_LIST.append([title[0], position[0], salary[0], experience, education, company[0]])

# 爬取boss列表页
def scrape_boss(url):
    try:
        chrome.get(url)
        time.sleep(4)
        parse_boss(chrome.page_source)
        # 爬取下一页，使用JS脚本完成翻页操作
        time.sleep(1)
        while (chrome.find_elements(By.XPATH, '//div[@class="search-job-result"]/div/div/div/a')[-1].get_attribute('class') != 'disabled'):
            chrome.execute_script('arguments[0].click()', chrome.find_elements(By.XPATH, '//div[@class="search-job-result"]/div/div/div/a')[-1])
            time.sleep(random.randint(2, 5)) # 这里时间可以留长些，有时页面加载时间较长
            parse_boss(chrome.page_source)
            time.sleep(random.randint(1, 4))
    except Exception as e:
        print(e)
    print("boss爬取完成！")


# 解析lagou列表页数据
def parse_lagou(html):
    root = etree.HTML(html)
    divs = root.xpath('//div[@id="jobList"]/div//div')  # 获取列表页
    # 遍历列表页中每一条数据，进行信息提取
    for div in divs:
        title_position = div.xpath('div[1]/div[1]//div[@class="p-top__1F7CL"]/a/text()')
        salary = div.xpath('div[1]/div[1]//div[@class="p-bom__JlNur"]/span/text()')
        experience_education = div.xpath('div[1]/div[1]//div[@class="p-bom__JlNur"]/text()')
        company = div.xpath('div[1]/div[2]/div[1]/a/text()')
        # 当不为[]时，按索引取值
        if title_position != []:
            title = title_position[0].split('[')[0]
            position = title_position[0].split('[')[1].split('·')[0]
            experience = experience_education[0].split('/')[0].strip()
            education = experience_education[0].split('/')[1].strip()
            print(title, position, salary[0], experience, education, company[0])
            LAGOU_LIST.append([title, position, salary[0], experience, education, company[0]])

# 爬取lagou列表页
def scrape_lagou(url, keyword):
    try:
        chrome.get(url)
        time.sleep(1)
        # 取消自动弹出的城市勾选
        cboxClose = chrome.find_element(By.XPATH, '//button[@id="cboxClose"]')
        if cboxClose:
            cboxClose.click()
        time.sleep(1)
        # 输入关键字并查询
        search_input = chrome.find_element(By.XPATH, '//input[@id="search_input"]')
        search_input.send_keys(keyword)
        time.sleep(1)
        search_button = chrome.find_element(By.XPATH, '//input[@id="search_button"]')
        search_button.click()
        # 解析并保存信息
        time.sleep(2)
        parse_lagou(chrome.page_source)
        # 爬取下一页，使用JS脚本完成翻页操作
        time.sleep(1)
        while (chrome.find_elements(By.XPATH, '//ul[@class="lg-pagination"]/li')[-1].get_attribute('aria-disabled') != 'true'):
            chrome.execute_script('arguments[0].click()', chrome.find_elements(By.XPATH, '//ul[@class="lg-pagination"]/li')[-1])
            time.sleep(random.randint(1, 3))
            parse_lagou(chrome.page_source)
            time.sleep(random.randint(1, 4))
    except Exception  as e:
        print("e")
    print("拉钩爬取完成！")


def scrape_data(keyword):
    '''
    使用selenium爬取主流招聘网站的信息
    :param keyword: 查询的关键字
    :return: 无
    '''

    # 爬取boss,直接传入带参数的地址，避免模拟登录时，地区被自动设置为当前ip所在的城市
    params = {
        'query': keyword,
        'city': "100010000"
    }
    boss_url = 'https://www.zhipin.com/web/geek/job?' + urlencode(params)
    scrape_boss(boss_url)

    # 爬取lagou,模拟浏览器点击操作，进入带参数的地址
    lagou_url = "https://www.lagou.com/"
    scrape_lagou(lagou_url, keyword)
    chrome.close()


def save_data(job_data):
    db = pymysql.connect(host='localhost', user='root', password='159831', port=3306)
    cursor = db.cursor()
    cursor.execute('show databases;')
    data = cursor.fetchall()
    # 若job_db数据库不存在，则创建
    flag = 1
    for db_ in data:
        if db_[0] == 'job_db':
            flag = 0
    if flag:
        cursor.execute('create database job_db;')

    # 进入job_db数据库,若表job_table已存在，删除
    cursor.execute('use job_db;')
    cursor.execute('show tables;')
    data = cursor.fetchall()
    flag = 0
    for tab in data:
        if tab[0] == 'job_table':
            flag = 1
    if flag:
        cursor.execute('drop table job_table;')

    # 新建表，并插入数据
    cursor.execute('create table job_table (职位名称 varchar(255), 城市 varchar(255), '
                   '薪资 varchar(255), 工作经验 varchar(255), '
                   '学历 varchar(255), 公司名称 varchar(255), '
                   '最低薪资 varchar(255))')

    # 逐行将数据写入数据库
    for i in range(job_data.shape[0]):
        data_row = job_data.iloc[i, :].to_dict()
        keys = ','.join(data_row.keys())
        values = ','.join(['%s'] * len(data_row))
        sql = 'insert into job_table ({keys}) values ({values})'.format(keys=keys, values=values)
        try:
            cursor.execute(sql, tuple(data_row.values()))
            db.commit()
        except:
            print('Failed')
            db.rollback()

    db.close()
    print("数据已保存至数据库!")


def process_save_data():
    '''
    清洗数据并保存至数据库
    '''
    data = pd.concat([pd.DataFrame(BOSS_LIST), pd.DataFrame(LAGOU_LIST)])
    data.columns = ["职位名称", "城市", "薪资", "工作经验", "学历", "公司名称"]
    # 剔除职位名称中没有爬虫关键字的数据
    data = data[data["职位名称"].str.contains("爬虫")]
    # 循环处理其他字段
    salary_down = []
    for i in range(data.shape[0]):
        # 提取城市名称
        data.iloc[i, 1] = data.iloc[i, 1].split("·")[0]
        # 获取最低薪资，后续以此为标准进行薪资分析
        sal_dw = data.iloc[i, 2].split("-")[0]
        salary_down.append(int(sal_dw[:-1] if 'k' in sal_dw else sal_dw))
        # 工作经验字段处理
        data.iloc[i, 3] = data.iloc[i, 3].replace("经验", ""). \
            replace("在校", "不限").replace("在校/应届", "不限"). \
            replace("不限/应届", "不限").replace("1个月", "1年以内"). \
            replace("2个月", "1年以内").replace("3个月", "1年以内"). \
            replace("6个月", "1年以内")
        # 学历字段处理
        data.iloc[i, 4] = data.iloc[i, 4].replace("不限", "学历不限"). \
            replace("中专/中技", "专科").replace("大专", "专科"). \
            replace("学历学历不限", "学历不限")
    data["最低薪资"] = salary_down
    # 剔除薪资中按天计薪的数据和异常数据
    data = data[~data["薪资"].str.contains("元/天")]
    data = data[~data["最低薪资"] < 100]
    # 保存数据至数据库
    save_data(data)


def main():
    scrape_data("爬虫")
    process_save_data()


if __name__ == '__main__':
    main()
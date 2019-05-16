# -*- coding: utf-8 -*-
#这是用于爬取微博评论的爬虫
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains  
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions as selexcept
import scrapy
from scrapy import Spider
from scrapy.http import HtmlResponse
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
from testSpider.items import CommentItem
from testSpider.spiders.utils import time_fix
import re
import time, random
from lxml import etree

class singleWeibo(scrapy.Spider):
    name = 'commentSpider'
    def __init__(self):              
        # 创建chrome参数对象
        opt = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=opt)
        self.driver.set_window_size(1000, 1080)
        wait = WebDriverWait(self.driver, 20)
        #weibo模拟登陆
        url = 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https://weibo.cn/'
        self.driver.get(url)
        username = wait.until(EC.presence_of_element_located((By.ID, 'loginName')))
        password = wait.until(EC.presence_of_element_located((By.ID, 'loginPassword')))
        submit = wait.until(EC.element_to_be_clickable((By.ID, 'loginAction')))
        username.send_keys('####') #微博账号
        password.send_keys('####') #微博密码
        submit.click()
        time.sleep(2)

    def closed(self, spider):
        print("spider closed")
        self.driver.close()
    
    def start_requests(self):
        pagenum1 = 1      #起始页数
        pagenum2 = 1000   #终止页数
        origin = '####'  #设定发布者昵称
        start_urls = ['https://weibo.cn/comment/H3h3HgPl5?uid=1640016932&&page={}'.format(str(i)) for i in range(pagenum1,pagenum2+1)]
        for url in start_urls:
            weibo_id = re.findall(r'https://weibo.cn/comment/(\w+)\?uid=(\d+)',url)[0][0]
            uid = re.findall(r'https://weibo.cn/comment/(\w+)\?uid=(\d+)',url)[0][1]
            yield Request(url=url, callback=self.parse, meta={'weibo_id': weibo_id,'uid':uid,'origin':origin})
    
    def parse(self, response):
        selector = Selector(response)
        comment_nodes = selector.xpath('//div[@class="c" and contains(@id,"C_")]')
        originweibo_id = response.meta['weibo_id']  #原微博的id，由字母组成
        originuser_id = response.meta['uid']        #原微博发布者的id，由数字组成
        origin = response.meta['origin']
        for comment_node in comment_nodes:
            comment_user_url = comment_node.xpath('./a[1]/@href').extract_first()
            if not comment_user_url:
                continue
            comment_item = CommentItem()  #对接Item
            comment_item['crawl_time'] = int(time.time())
            #标注爬取的微博url
            comment_item['weibo_url'] = 'https://weibo.cn/' + originuser_id + '/' + originweibo_id
            comment_item['comment_user'] = comment_node.xpath('a[1]/text()').extract_first()
            user_url = re.findall(r'.*?/(\w+)(?!/)', comment_user_url)[0] 
            comment_item['comment_user_id'] = user_url
            #获取整个评论文本
            comment_item['content'] = comment_node.xpath('.//span[@class="ctt"]').xpath('string(.)').extract_first()
            comment_item['_id'] = comment_node.xpath('./@id').extract_first()
            created_at = comment_node.xpath('.//span[@class="ct"]/text()').extract_first()
            comment_item['created_at'] = time_fix(created_at.split('\xa0')[0])
            comment_like = comment_node.xpath('.//span[@class="cc"]/a[contains(text(),"赞[")]/text()').extract_first()
            comment_item['like'] = int(re.search('\d+', comment_like).group())
            #评论对象用户
            try:
                #间接转发
                comment_item['comment_to'] = comment_node.xpath('span[@class="ctt"]/a[1]/text()').extract_first().split('@')[1]
            except Exception as error11:
                #直接转发
                comment_item['comment_to'] = origin
            yield comment_item


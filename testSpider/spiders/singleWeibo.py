# -*- coding: utf-8 -*-
#这是用于爬取微博转发的爬虫
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
from testSpider.items import RepostItem
from testSpider.spiders.utils import time_fix
import re
import time, random
from lxml import etree

class singleWeibo(scrapy.Spider):
    name = 'repostSpider'

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
        pagenum1 = 1         #设定起始页数
        pagenum2 = 1000      #设定终止页数
        origin = '####'  #设定发布者昵称
        start_urls = ['https://weibo.cn/repost/Hr5djzlEU?uid=6157151766&&page={}'.format(str(i)) for i in range(pagenum1,pagenum2+1)]
        for url in start_urls:
            weibo_id = re.findall(r'https://weibo.cn/repost/(\w+)\?uid=(\d+)',url)[0][0]
            uid = re.findall(r'https://weibo.cn/repost/(\w+)\?uid=(\d+)',url)[0][1]
            yield Request(url=url, callback=self.parse, meta={'weibo_id': weibo_id,'uid':uid,'origin':origin})

    def parse(self, response):
        j = 0  #用于控制一页内每条数据的排序
        selector = Selector(response)
        repost_nodes = selector.xpath('//span[@class="cc" ]/..')
        pageinfo1 = selector.xpath('string(//*[@id="pagelist"]/form/div/text()[last()])').extract() 
        pageinfo1 = pageinfo1[0].split('\xa0')[1]
        pageinfo = re.findall(r'\d+',pageinfo1)
        pagenum_cur = int(pageinfo[0])       #当前页面是第几页
        print('现在在爬取第 %d 页' % pagenum_cur)
        pagenum_max = int(pageinfo[1])       #总共有多少页
        maxnum1 = selector.xpath('.//span[contains(@class,"pms") and contains(@id,"rt")]/text()').extract()
        maxnum= ''.join(maxnum1).split('\xa0')[0]
        maxnum = int(re.search(r'\d+',maxnum).group(0))   #总转发数
        originweibo_id = response.meta['weibo_id']  #原微博的id，由字母组成
        originuser_id = response.meta['uid']        #原微博发布者的id，由数字组成
        origin = response.meta['origin']
        for repost_node in repost_nodes:
            repost_user_url = repost_node.xpath('./a[1]/@href').extract_first()
            if not repost_user_url:
                continue
            repost_item = RepostItem()   #对接Item
            repost_item['crawl_time'] = int(time.time())
			#标记爬取的微博
            repost_item['weibo_url'] = 'https://weibo.cn/' + originuser_id + '/' + originweibo_id
            repost_item['repost_user'] = repost_node.xpath('a[1]/text()').extract_first()
            user_url = re.findall(r'.*?/(\w+)(?!/)', repost_user_url)[0] #
            repost_item['repost_user_id'] =  user_url
            #获取整个转发文本
            content1 = repost_node.css('div[class="c"]::text').extract()
            repost_item['content'] = ''.join(content1).split('\xa0')[0]
            #获取转发时间
            created_at = repost_node.xpath('.//span[@class="ct"]/text()').extract_first()
            repost_item['created_at'] = time_fix(created_at.split('\xa0')[1])
            #获取赞的数目
            repost_like = repost_node.xpath('.//span[@class="cc"]/a[contains(text(),"赞[")]/text()').extract_first()
            repost_item['like'] = int(re.search('\d+', repost_like).group())
            #转发前置用户
            try:
                #间接转发
                repost_item['repost_from'] = repost_node.xpath('a[2]/text()').extract_first().split('@')[1]
            except AttributeError as error11:
                #直接转发
                repost_item['repost_from'] = origin
            #在一页之中，最上面的元素，离发布时间越远
            #理论上一页应当有10页数据
            repost_item['accumulated_reposts'] = (maxnum%10) +(pagenum_max - pagenum_cur)*10 - j 
            j = j+1
            yield repost_item

    

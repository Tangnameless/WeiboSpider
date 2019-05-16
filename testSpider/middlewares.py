# -*- coding: utf-8 -*-

from scrapy import signals
import time,random


class TestspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TestspiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

#这里是我们的js脚本开始执行的地方
from scrapy.http import HtmlResponse
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

#在Middleware里面的process_request()方法里对每个抓取请求进行处理，启动浏览器并进行页面渲染，再将渲染后的结果构造一个HtmlResponse对象
#下载中间件返回的是response对象的时候，之后的下载中间件将不会被继续执行，而是直接返回response对象。
class JSPageMiddleware(object):
    def process_request(self,request,spider):
        if spider.name =="repostSpider" or "commentSpider":
            #每一页延迟2~2.5s
            time.sleep(0.1)
            spider.driver.get(request.url)
            try:
                #每个正常加载的页面一定能找到首页这一横条
                spider.driver.find_element_by_class_name('n')
            except Exception as err1:
                print(err1)
                spider.logger.error('错误代码408，ip 被封了!!!请更换ip,或者停止程序...')
                #启用代理ip(如果有)
                #ip被封锁，休眠60s
                time.sleep(60)
                return request
            #print(spider.driver.page_source)
            #未进入错误分支，则说明正常获取页面
            #不存在大量空白页的状况就注释掉，因为极大降低运行速度
            #n = 0
            #while n >= 0 and n<5:
                #try:
                    #查看这一页是否刷出了数据，如果没有数据，则刷新至有数据为止,循环超过5次则放弃这一页
                    #spider.driver.find_element_by_xpath('//span[@class="cc" ]/..')   
                    #break
                #except Exception as err2:
                    #print(err2)
                    #spider.logger.error('这一页没有加载出数据')
                    #spider.driver.get(request.url)      #刷新页面  
                    #n = n+1
                    #time.sleep(2)        
            dur = random.random()
            time.sleep(0.5*dur)
            return HtmlResponse(url=spider.driver.current_url,body=spider.driver.page_source, encoding="utf-8",request=request)


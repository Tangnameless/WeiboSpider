# -*- coding: utf-8 -*-

# Scrapy settings for testSpider project

BOT_NAME = 'testSpider'

SPIDER_MODULES = ['testSpider.spiders']
NEWSPIDER_MODULE = 'testSpider.spiders'


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

DOWNLOADER_MIDDLEWARES = {
'testSpider.middlewares.JSPageMiddleware': 1,
}
DEFAULT_REQUEST_HEADERS = {
'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}

#默认导出转发数据，爬取评论数据存入MongoDB中再自行导出
FEED_EXPORT_FIELDS=['repost_user','weibo_url','created_at','content','like','repost_from']

ITEM_PIPELINES = {

    'testSpider.pipelines.TestspiderPipeline':300,
    'testSpider.pipelines.MongoDBPipeline': 301,

}

# 修改编码为utf-8 防止中文写入乱码
FEED_EXPORT_ENCODING = 'utf-8-sig'

# MongoDb 配置
LOCAL_MONGO_HOST = '127.0.0.1'
LOCAL_MONGO_PORT = 27017
DB_NAME = 'weibo1'      #设置数据库名称


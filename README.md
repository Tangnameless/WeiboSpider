# noobWeiboSpider
项目地址：https://github.com/Tangnameless/noobWeiboSpider  
**特此声明，本项目主要参考了nghuyong/WeiboSpider项目中的simple分支**  
参考项目地址：https://github.com/nghuyong/WeiboSpider  
上传的主要目的也是记录一下自己学习大佬代码的成果和熟悉Git的使用  

## 项目说明
该项目为基于scrapy的单账号微博爬虫，爬取的站点是 weibo.cn。主要思路是通过selenium模拟人的登陆，并让程序自动访问微博页面，将抓取的网页源代码组成response对象。  
原项目中使用了PhantomJS，但是听说已经停止维护了，而且chorme也有无头浏览模式，遂改用chorme了。但是chomre的headless模式比起正常模式要慢很多，不推荐使用无头浏览模式。  
没有设置账号池（穷）！  
没有设置代理IP（穷）！    
总之是一个适合穷人的，速率尚可的爬虫。    
爬取的对象主要为微博文本，即热门微博的转发数据与评论数据。  
每一条微博建立一个数据库，内设两个表分别存储转发和评论数据。  
singleWeibo.py和singleWeibo_comment.py 分别为爬取微博转发数据和微博评论数据的爬虫。    

## 克隆环境 && 安装依赖
python == 3.6.8  
scrapy == 1.5.2  
pymongo == 3.7.2  
lxml == 4.3.2  
selenium == 3.141.0  

```
git clone git@github.com:Tangnameless/noobWeiboSpider.git
```

同时还需要安装MongoDB和chorme，请自行百度。  
特别要注意chorme和chormediver之间版本的对应问题。

## 数据字段说明
### 1.转发数据
|字段 | 说明 |
|--|--|
|repost_user_id | 转发用户的id|
|repost_user |转发用户的昵称|
|content| 评论的内容|
|weibo_url|转发的微博的url|
|created_at |转发时间|   
 |crawl_time|抓取时间戳|
|like|评论点赞数|
|repost_from|转发前置|
|accumulated_reposts|本条数据对应的累计转发量|

### 2. 评论数据
|字段 | 说明 |
|--|--|
|comment_user_id | 评论用户的id|
|comment_user |评论用户的昵称|
|content| 评论的内容|
|weibo_url|评论的微博的url|
|created_at |评论发表时间|    |crawl_time|抓取时间戳|
|like|评论点赞数|
|comment_to|评论的对象用户|

## 如何使用
以下面这条微博为例
### 将网页版微博链接转换为weibo.cn中的链接
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190517154401254.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5NjEwOTE1,size_16,color_FFFFFF,t_70)  
其在微博网页版中的url为：  
https://weibo.com/1686546714/Huz8eB7lU?type=comment#_rnd1558077460937  
根据url中的**微博id**和**用户id**，将weibo.com的url改为weibo.cn中的url：  
https://weibo.cn/repost/Huz8eB7lU?uid=1686546714&&page=1  
根据要爬取的是评论还是转发，写入comment或repost  

### 更改数据库设置
![在这里插入图片描述](https://img-blog.csdnimg.cn/2019051716383034.png)
### 设置微博登录账号
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190517172918788.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5NjEwOTE1,size_16,color_FFFFFF,t_70)
### 设置爬取微博参数
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190517172959185.PNG?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5NjEwOTE1,size_16,color_FFFFFF,t_70)
### 运行结果
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190517161310324.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5NjEwOTE1,size_16,color_FFFFFF,t_70)
### 存入数据库的结果
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190517160658861.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5NjEwOTE1,size_16,color_FFFFFF,t_70)
# 速度说明
weibo.cn站点中，一页有10条数据

设置     | 配置值
-------- | -----
账号数 | 1
CONCURRENT_REQUESTS	  | scrapy默认
每页数据下载延迟  | 0.1s
每分钟抓取网页量|74+
理论上每分钟抓取数据量|740
理论上一天抓取数据量|**100w+**

实际速度和你自己电脑的网速/CPU/内存有很大关系。  
weibo.cn中数据总是有缺损的，理论抓取量是按页数来算的。    
weibo.cn中经常会出现一页数据加载不够10条的情况。
如示例微博爬取1000页后实得8908条，获取率约为89%。  
该项目使用selenium，延迟太低也没有意义，浏览器渲染页面，scrapy运行都需要花费一定时间，实际延迟大于0.1s。  
具体爬一页数据暂停多长时间需要自己测试。
以我的经验来说，爬取一页数据延迟2-3s不会被微博封IP，但最近爬的快些微博也能容忍。    

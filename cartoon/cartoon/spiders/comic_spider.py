#!/usr/bin/env python
# coding: utf-8

# In[1]:


# -*- coding: utf-8 -*-

import re
import scrapy
# from scrapy import Selector
from Spider.cartoon.cartoon.items import ComicItem
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy_redis.spiders import RedisSpider
# In[3]:


class ComicSpider(RedisSpider):
    name = 'comic'
    redis_key = 'ComicSpider:comic_urls'

    def __init__(self):
        self.allowed_domains = ['comic.kukudm.com']
        #self.start_urls = ['http://comic.kukudm.com/comiclist/2125/']
        self.start_urls = ['http://comic.kukudm.com/comiclist/2125/50336/1.htm']
        # 匹配图片地址的正则表达式

    # 从start_requests发送请求
    def start_requests(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(self.start_urls[0])
        page_source = driver.page_source
        # 退出
        driver.quit()
        a = BeautifulSoup(page_source, 'lxml')
        item = ComicItem()
        print("""




                                    """)
        b = a.find('td',valign='top')
        c = b.img['src']  # img_url
        d = b.text
        e = re.findall(u'共(\d+)页',d)[0]  # page_num
        f = re.findall(u'当前第(\d+)页',d)[0]  # page_now
        g = re.findall(u'(.+) 2话',d)[0]  # dir_name
        print('here')
        print(c,'\n',e,'\n',f,'\n',g)
        print("""




                                """)
        # 获取章节的第一页的图片链接
        # 将获取的章节的第一页的图片链接保存到img_url中
        item['link_url'] = self.start_urls[0]
        item['img_url'] = c
        item['img_page'] = f
        item['dir_name'] = g
        page_num = e
        # 返回item，交给item pipeline下载图片
        yield item
        # 根据页数，整理出本章节其他页码的链接
        pre_link = item['link_url'][:-5]
        for each_link in range(2, int(page_num) + 1):
            new_link = pre_link + str(each_link) + '.htm'
            # 根据本章节其他页码的链接发送Request请求，用于解析其他页码的图片链接，并传递item
            yield scrapy.Request(url = new_link, callback = self.parse)

    # 解析获得本章节其他页面的图片链接
    def parse(self, response):
        # 获取章节的第一页的链接
        item = ComicItem()
        item['link_url'] = response.url
        print("""




                    """)
        a = BeautifulSoup(str(response.text),'lxml')
        b = a.find('td', valign='top')
        c = b.img['src']  # img_url
        d = b.text
        e = re.findall(u'共(\d+)页', d)[0]  # page_num
        f = re.findall(u'当前第(\d+)页', d)[0]  # page_now
        g = re.findall(u'(.+) 2话', d)[0]  # dir_name
        print('here')
        print(c, '\n', e, '\n', f, '\n', g)
        print("""




                                """)
        # 获取章节的第一页的图片链接
        # 将获取的章节的第一页的图片链接保存到img_url中
        item['img_url'] = c
        item['img_page'] = f
        item['dir_name'] = g
        # 返回item，交给item pipeline下载图片
        yield item

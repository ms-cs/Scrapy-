# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from Spider.cartoon.cartoon import settings
from scrapy import Request
import requests
import os


class ComicImgDownloadPipeline(object):
    def process_item(self, item, spider): # 如果获取了图片链接，进行如下操作
        if 'img_url' in item:
            images = []
            # 文件夹名字
            dir_path = '%s/%s' % (settings.IMAGES_STORE, item['dir_name'])
            # 文件夹不存在则创建文件夹
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                # 获取每一个图片链接
            image_file_name = item['img_page']
            # 图片保存路径
            file_path = '%s/%s.jpg' % (dir_path, str(image_file_name))
            images.append(file_path)
            # 保存图片
            with open(file_path, 'ab') as handle:
                response = requests.get(url = item['img_url'])
                handle.write(response.content)
                handle.close()
                # 返回图片保存路径
            item['image_paths'] = images
        return item

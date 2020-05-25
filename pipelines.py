# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import scrapy
import logging
from urllib.parse import urlparse
from scrapy.pipelines.images import ImagesPipeline


class BabysImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if 'images' in item:
            for image_url, image_dir in item['images'].items():
                request = scrapy.Request(url=image_url)
                request.meta['image_dir'] = image_dir
                yield request

    def file_path(self, request, response=None, info=None):
        return '/' + request.meta['image_dir'] + '/' + os.path.basename(urlparse(request.url).path)
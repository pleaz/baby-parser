# -*- coding: utf-8 -*-
import scrapy
from babys.items import BabysItem


class BabySpider(scrapy.Spider):
    name = 'baby'
    allowed_domains = ['babywoods.ru']
    start_urls = ['http://babywoods.ru/shop']

    def parse(self, response):
        menu_items = response.xpath('//nav[@class="shop-menu vertical"]/ul//li[contains(@class, "shop-menu-item")]/a/@href').extract()
        for menu_item in menu_items:
            if menu_item is not '#':
                yield scrapy.Request(
                    menu_item,
                    callback=self.parse_category
                )

    def parse_category(self, response):
        products = response.xpath('//div[contains(@class, "products-list")]/div[@class="static-grid-item"]//a/@href').extract()
        for product in products:
            yield scrapy.Request(
                product,
                callback=self.parse_product
            )

    @staticmethod
    def parse_product(response):
        item = BabysItem()
        images = response.xpath('//div[contains(@class, "product-main-image")]/img')
        for image in images:
            base_source = image.xpath('@data-base-path')
            base = base_source.extract_first()
            filename = image.xpath('@data-file-name').extract_first()
            # product_id = base_source.re('/products/(\d+)/images/')[0]
            product_name = image.xpath('@alt').extract_first()
            url = 'http:' + base + '3-' + filename
            item['images'] = {url: product_name}
            yield item

# -*- coding: utf-8 -*-
import scrapy
import json
import re

from AMAZON.items import AmazonItem


class AmazonspiderSpider(scrapy.Spider):
    name = 'amazonSpider'
    allowed_domains = ['www.amazon.com']
    # start_urls = ["https://www.amazon.com/dp/B07JJPBLMR"]
    start_urls = [
        "https://www.amazon.com/dp/B07DYW1WG7",
        "https://www.amazon.com/dp/B00605L6Z2",
        "https://www.amazon.com/dp/B07L4ZSCS3"
        ]

    def parse(self, response):
        '''
        处理母asin
        '''
        
        yield scrapy.Request(response.url, callback=self.parse_detail)

    def parse_detail(self, response):
        '''
            提取所有的script标签内容，并且在内容中找到包含dimensionToAsinMap这一行的内容
        '''
        # 提取商品所在目录
        item = AmazonItem()
        item['ASIN'] = response.url.split('/')[-1]

        label = response.xpath(
            '//div[@id="bylineInfo_feature_div"]/div/a/@href'
            ).extract()
        products = response.xpath('//div[@id="centerCol"]')
        sale_rank_total = response.xpath(
            '//li[@id="SalesRank"]/text()'
            ).extract()
        sale_rank_detail = response.xpath('//li[@id="SalesRank"]/ul/li')
        product_star = products.xpath(
            './/span[@id="acrPopover"]/@title'
            ).re(r'(\d\.\d)')
        product_fit = products.xpath(
            './/a[@id="HIF_link"]/text()'
            ).re(r'\d+|\d\.\d')
        product_fit_info = products.xpath(
            '//table[@id="fitRecommendationHistogramTable"]/tr/td[@class="a-span2 a-nowrap"]/span/text()'
            ).extract()
        product_ask_num = products.xpath(
            './/a[@id="askATFLink"]/span/text()'
            ).re(r'(\d+)')
        product_review_num = products.xpath(
            './/span[@id="acrCustomerReviewText"]/text()'
            ).re(r'(\d+)')
        best_seller_info = products.xpath(
            './/div[@id="zeitgeistBadge_feature_div"]/div[@class="badge-wrapper"]/a/@title'
            ).extract()
        if len(sale_rank_total) > 0:
            item['total_rank'] = re.findall(r'\d+', sale_rank_total[1])
            item['total_rank_info'] = re.findall(
                r'in (.+) \(', sale_rank_total[1])
        item['label'] = label[0].split("=")[-1] if label else None
        item['product_star'] = product_star[0] if product_star else None
        item['product_fit'] = product_fit[0] if product_fit else None
        item['product_ask_num'] = product_ask_num[0]\
            if product_ask_num else None
        item['product_review_num'] = product_review_num[0]\
            if product_review_num else None
        if best_seller_info:
            item['is_best_seller'] = 1
            item['best_seller_title'] = best_seller_info[0]
        else:
            item['is_best_seller'] = 0
            item['best_seller_title'] = None

        rank_list = []
        rank_list_detail = []
        for each in sale_rank_detail:
            rank = each.xpath(
                './/span[@class="zg_hrsr_rank"]/text()'
                ).re(r'\d')
            rank_list.append(rank)
            detail = each.xpath(
                './/span[@class="zg_hrsr_ladder"]/a/text()'
                ).extract()
            rank_list_detail.append(detail)
        item['detail_rank'] = rank_list
        item['detail_rank_info'] = rank_list_detail

        return item

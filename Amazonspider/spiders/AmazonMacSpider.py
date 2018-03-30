# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from Amazonspider.items import AmazonspiderItem
import re


class AmazonmacSpider(Spider):
    name = 'AmazonMacSpider'
    allowed_domains = ['www.amazon.com']
    start_urls = ['https://www.amazon.com/s/ref=sr_pg_1?fst=p90x%3A1&rh=n%3A172282%2Ck%3Amacbook&keywords=macbook&ie=UTF8&qid=1522246332']

    def parse(self, response):

        # 获取商品详情页URL
        urls = response.xpath('//a[@class="a-size-small a-link-normal a-text-normal"]/@href').extract()
        for url in urls:
            if 'customerReviews' in url:
                yield Request(url, callback=self.product_page_parse)


        # 获取下一商品列表页的URL, 回调index_page_parse
        try:
            next_page_url_part = response.xpath('//*[@id="pagnNextLink"]/@href').extract()
            next_page_url = 'https://www.amazon.com' + next_page_url_part[-1]
            yield Request(next_page_url, callback=self.parse)

        except:
            print('No More next page!')
            pass


    def product_page_parse(self, response):

        customReview_url_part = response.xpath('//*[@id="reviews-medley-footer"]/div/a/@href').extract()
        customReview_url = 'https://www.amazon.com' + customReview_url_part[-1]
        yield Request(customReview_url, callback=self.customReview_parse)

    def customReview_parse(self, response):

        # 获取所有评论,星级,时间,有用人数

        item = AmazonspiderItem()

        product_name = response.xpath('//*[@id="cm_cr-product_info"]/div/div[2]/div/div/div[2]/div[1]/h1/a/text()').extract()


        for info in response.xpath('//*[@id="cm_cr-review_list"]/div'):
            text = info.xpath('.//div[@class="a-row review-data"]//text()').extract()
            if len(text) > 0:
                tmp = info.xpath('.//div[@class="a-row"]//text()').extract()
                try:
                    useful = info.xpath('.//*[@data-hook="helpful-vote-statement"]/text()').extract()[-1]
                    useful_num = re.findall('\d+', useful)[-1]
                except:
                    useful_num = 0

                item['product_name'] = product_name[-1]
                item['review_star'] = tmp[0]
                item['review_time'] = tmp[4]
                item['useful_num'] = useful_num
                item['product_review'] = text[-1]

                yield item
        try:
            next_url_part = response.xpath('.//li[@class="a-last"]/a/@href').extract()
            next_url = 'https://www.amazon.com' + next_url_part[-1]
            yield Request(next_url, callback=self.customReview_parse)
        except:
            print(next_url_part)
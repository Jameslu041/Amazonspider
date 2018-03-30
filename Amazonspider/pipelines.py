# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import log
import pymysql
import pymysql.cursors
import codecs
from twisted.enterprise import adbapi
import pymongo


class MongoPipeline(object):

    collection_name = 'product'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # 去重
        # self.db['product'].update({'url_token': item['url_token']}, {'$set': item}, True)
        self.db[self.collection_name].insert(dict(item))
        return item


# class AmazonspiderPipeline(object):
#     # def process_item(self, item, spider):
#     #     return item
#
#     @classmethod
#     def from_settings(cls, settings):
#         '''1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。
#            2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
#            3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
#         dbparams = dict(
#             host=settings['MYSQL_HOST'],  # 读取settings中的配置
#             db=settings['MYSQL_DBNAME'],
#             user=settings['MYSQL_USER'],
#             passwd=settings['MYSQL_PASSWD'],
#             charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
#             cursorclass=pymysql.cursors.DictCursor,
#             use_unicode=False,
#         )
#         dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
#         return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到
#
#     def __init__(self, dbpool):
#         self.dbpool = dbpool
#
#     # pipeline默认调用
#     def process_item(self, item, spider):
#         d = self.dbpool.runInteraction(self._conditional_insert, item, spider)  # 调用插入的方法
#         log.msg("-------------------连接好了-------------------")
#         d.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
#         d.addBoth(lambda _: item)
#         return d
#
#     def _conditional_insert(self, conn, item, spider):
#         log.msg("-------------------打印-------------------")
#
#         conn.execute("insert into test(product_name, review_star, review_time, useful_num, product_review) values(%s, %s, %s, %s, %s)",
#                      (item['product_name'], item['review_star'], item['review_time'], item['useful_num'], item['product_review']))
#         log.msg("-------------------一轮循环完毕-------------------")
#
#     def _handle_error(self, failue, item, spider):
#         print(failue)
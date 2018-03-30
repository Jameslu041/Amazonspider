# Amazonspider
2018.03.30

背景是校内实训项目需要爬取亚马逊的商品评论进行语义情感极性分析,
本次爬取初始网站是人为指定搜索关键词mac,
主要爬取的字段如下

id | product_name| product_review | review_star |review_time | useful_num
---|---|---|---|---|---
编号| 商品名字 | 商品的评论 | 商品星级 | 评论时间 | 觉得该评论有帮助人数

可改进处:
1. 添加代理IP池,切ip来对抗亚马逊反爬
2. 断点续爬
...

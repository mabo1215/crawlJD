# - * - coding: utf-8 - * -

__author__ = "JD Scrawler"

from scrapy.spiders import CrawlSpider
from JDSpider.items import JdspiderItem
from scrapy.selector import Selector
from scrapy.http import Request
import requests
import re, json

class JdSpider(CrawlSpider):
    name = "JDSpider"
    redis_key = "JDSpider:start_urls"
    start_urls = ["http://list.jd.com/list.html?cat=1315,1345,1364"]
	#http://book.jd.com/booktop/0-0-0.html?category=20003-0-0-0-10001-1#comfort"]

    def parse(self, response):
        item = JdspiderItem()
        selector = Selector(response)
        Cates = selector.xpath('/html/body/div[8]/div/div[2]/div[1]/div/div[2]/ul/li')
        for each in Cates:
			bPrice = each.xpath('/div/div[@class="p-price"]/strong[1]/text()').extract()
			pName = each.xpath('/div/div[@class="p-name"]/strong[1]/i/text()').extract()
            #temphref = each.xpath('div[@class="p-detail"]/a/@href').extract()
            #temphref = str(temphref)
            #BookID = str(re.search('com/(.*?)\.html',temphref).group(1))
            #json_url = 'http://p.3.cn/prices/mgets?skuIds=J_'+ BookID
            #r = requests.get(json_url).text
            #data = json.loads(r)[0]
            #price = data['m']
            #PreferentialPrice = data['p']
			item['Price'] = bPrice
			item['Name'] = pName 
			#item['author'] = author
            #item['press'] = press
            #item['BookID'] = BookID
            #item['price'] = price
            #item['PreferentialPrice'] = PreferentialPrice
			yield item

        nextLink = selector.xpath('/html/body/div[8]/div[1]/div[2]/div[1]/div/div[3]/div/span/a[2]/@href').extract()
        if nextLink:
            nextLink = nextLink[0]
            print(nextLink)
            yield Request(nextLink,callback=self.parse)
            #num = each.xpath('div[@class="p-num"]/text()').extract()
            #price = each.xpath('div[@class="p-detail"]/dl[1]/dd/a[1]/text()').extract()
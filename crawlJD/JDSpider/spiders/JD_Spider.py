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
	start_urls = ["http://www.cnamall.cn/category.php?id=1"]
	#http://book.jd.com/booktop/0-0-0.html?category=20003-0-0-0-10001-1#comfort"]
	
	def parse(self, response):
		item = JdspiderItem()
		selector = Selector(response)
		Cates = selector.xpath('/html/body/div[7]/div[5]/div[1]/form/div/ul/li')
		for each in Cates:
			bPrice = selector.xpath('div/div[2]/div[2]/em[1]/text()').extract()
				#each.xpath('/div[@class="gl-i-wrap j-sku-item"]/div[@class="p-price"]/strong[@class="J_price"]/i/text()').extract()
			pName = selector.xpath('div/div[2]/div[1]/a/text()').extract()
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

		nextLink = selector.xpath('/html/body/div[7]/div[5]/form[1]/div/a[2]/@href').extract()
		#/html/body/div[@id="J_searchWrap"]/div[@id="J_container"]/div[@id="J_main"]/div[@class="m-list"]/div[@class="ml-wrap"]/div[@class="page clearfix"]/div[@id="J_bottomPage"]/span[@class="p-num"]/a[@class="pn-next"]/@href').extract()
		#/html/body/div[8]/div[1]/div[2]/div[1]/div/div[3]/div/span/a[2]/@href'
		if nextLink:
			nextLink = nextLink[0]
			print(nextLink)
			yield Request(nextLink,callback=self.parse)
            #num = each.xpath('div[@class="p-num"]/text()').extract()
            #price = each.xpath('div[@class="p-detail"]/dl[1]/dd/a[1]/text()').extract()
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
	start_urls = ["https://www.seek.co.nz/jobs-in-information-communication-technology/developers-programmers/in-new-zealand/#dateRange=999&workType=0&industry=6281&occupation=6287&graduateSearch=false&salaryFrom=0&salaryTo=999999&salaryType=annual&companyID=&advertiserID=&advertiserGroup=&keywords=web+developer&page=1&displaySuburb=&seoSuburb=&where=All+New+Zealand&whereId=3001&whereIsDirty=false&isAreaUnspecified=false&location=3001&area=&nation=3001%2C3001&sortMode=KeywordRelevance&searchFrom=quick&searchType="]
	#http://book.jd.com/booktop/0-0-0.html?category=20003-0-0-0-10001-1#comfort"]
	
	def parse(self, response):
		item = JdspiderItem()
		selector = Selector(response)
		pName = selector.xpath('/html/body/div[@id="bodyContainer"]/div[@id="bindingRoot"]/div[@class="grid_12 l-clearfix l-row"]/div[@id="job-listing-wrapper"]/div[@class="jobmail-signed-in jobs-exist first-page premium-jobs-exist no-tier1-jobs"]/section[@id="jobsListing"]/div[@class="jobs-list jobs-list-primary"]/article[@class="experimental-fade experimental-fade-completed"][1]/dl/dd[1]/p[@class="job-description"]/text()').extract()	
		item['Name'] = pName
		yield item
		#Cates = selector.xpath('/html/body/div[@id="bodyContainer"]/div[@id="bindingRoot"]/div[@class="grid_12 l-clearfix l-row"]/div[@id="job-listing-wrapper"]/div[@class="jobmail-signed-in jobs-exist first-page premium-jobs-exist no-tier1-jobs"]/section[@id="jobsListing"]/div[@class="jobs-list jobs-list-premium"][1]/article')
		#for each in Cates:
		#	bPrice = each.xpath('dl/dd[1]/ul[@class="bullet-points"]/li[1]/text()').extract()	
		#	pName = each.xpath('dl/dd[1]/h2/a[@class="job-title"]/text()').extract()		
			#temphref = each.xpath('div[@class="p-detail"]/a/@href').extract()
			#temphref = str(temphref)
			#BookID = str(re.search('com/(.*?)\.html',temphref).group(1))
			#json_url = 'http://p.3.cn/prices/mgets?skuIds=J_'+ BookID
			#r = requests.get(json_url).text
			#data = json.loads(r)[0]
			#price = data['m']
			#PreferentialPrice = data['p']
		#	item['Price'] = bPrice
		#	item['Name'] = pName
			#item['author'] = author
            #item['press'] = press
            #item['BookID'] = BookID
            #item['price'] = price
            #item['PreferentialPrice'] = PreferentialPrice
		#yield item

		nextLink = selector.xpath('/html/body/div[7]/div[5]/form[1]/div/a[2]/@href').extract()
		#/html/body/div[@id="J_searchWrap"]/div[@id="J_container"]/div[@id="J_main"]/div[@class="m-list"]/div[@class="ml-wrap"]/div[@class="page clearfix"]/div[@id="J_bottomPage"]/span[@class="p-num"]/a[@class="pn-next"]/@href').extract()
		#/html/body/div[8]/div[1]/div[2]/div[1]/div/div[3]/div/span/a[2]/@href'
		if nextLink:
			nextLink = nextLink[0]
			print(nextLink)
			yield Request(nextLink,callback=self.parse)
            #num = each.xpath('div[@class="p-num"]/text()').extract()
            #price = each.xpath('div[@class="p-detail"]/dl[1]/dd/a[1]/text()').extract()
import scrapy

from scrapy.loader import ItemLoader
from ..items import HipotekarnabankaItem
from itemloaders.processors import TakeFirst


class HipotekarnabankaSpider(scrapy.Spider):
	name = 'hipotekarnabanka'
	start_urls = ['https://www.hipotekarnabanka.com/obavjestenja']

	def parse(self, response):
		post_links = response.xpath('//article//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//ul[@class="pagination"]/li/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="text"]//text()[normalize-space() and not(ancestor::h4)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//h4[contains(@class, "date")]/text()').get()
		date = date.split(',')[1]

		item = ItemLoader(item=HipotekarnabankaItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()

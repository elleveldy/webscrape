import scrapy


class OddsSpider(scrapy.Spider):
	name = "oddsValues"

	def start_requests(self):
		urls = [
			'http://www.betmma.tips/free_ufc_betting_tips.php?Event=233',
		]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		page = response.url.split("/")[-2]
		filename = self.name+'-%s.html' % page
		with open(filename, 'wb') as f:
			f.write(response.body)
		self.log('Saved file %s' % fWilename)
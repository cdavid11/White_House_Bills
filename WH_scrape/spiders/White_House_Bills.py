from __future__ import unicode_literals
import scrapy
from bs4 import BeautifulSoup
import twitter


class Bill_Spider (scrapy.Spider):

	name = "White_House_Bills"

	def start_requests (self):

		url = "https://www.whitehouse.gov/briefing-room/signed-legislation"
		yield scrapy.Request(url=url, callback=self.parse)

	def parse (self, response):

		soup = BeautifulSoup(response.body, 'html.parser')
		panel = soup.find("div", {"class":"view-content"})
		bill = panel.find("div", {"class":"views-row views-row-1 views-row-odd views-row-first"})

		name = bill.a.text
		link = bill.a['href']
		print(name)
		print(link)

		to_tweet = "#DonaldTrump has signed: " + name + "\nhttps://www.whitehouse.gov" + link

		consumer_key='bx34EHcGqcKr8ZY2KBuS8hamL'
		consumer_secret='POqFlrQmur0fVtsZDIN2Aji79y1p55FNXB9yXvtZrynSzj4IW5'
		access_token_key='884782153904648192-nqr44xrASvX3Jg3q79DwMxEaOLcXR8k'
		access_token_secret='oGxxJFHmxOXZx5E8vvSpkwILCUFpILv5GuA9MKh3OTc9u'

		api = twitter.Api(consumer_key, consumer_secret, access_token_key, access_token_secret)
		status = api.PostUpdate(to_tweet)
		print(status.text)


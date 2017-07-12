from __future__ import unicode_literals
import scrapy
from bs4 import BeautifulSoup
import twitter
from auth import auth


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

		to_tweet = "#DonaldTrump has signed: seeing what sort of riddiculosueresfsdfsefes message that I'll get for having a tweet that is way way way wayw ay awy w too long yesah" + name + "\nhttps://www.whitehouse.gov" + link

		a = auth()

		api = twitter.Api(a.consumer_key, a.consumer_secret, a.access_token_key, a.access_token_secret)
		status = api.PostUpdate(to_tweet)
		print(status.text)


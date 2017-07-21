#!/usr/bin/python
from __future__ import unicode_literals
import scrapy
from bs4 import BeautifulSoup
from pymongo import MongoClient
import twitter
from auth import auth
import time


class Bill_Spider (scrapy.Spider):

				name = "White_House_Bills"
				connection = MongoClient()
				db = connection['Bills']
				bills = db.bills

				def start_requests (self):

					url = "https://www.whitehouse.gov/briefing-room/signed-legislation"
					yield scrapy.Request(url=url, callback=self.parse, meta={"sorv":"s"})
					url = "https://www.whitehouse.gov/briefing-room/vetoed-legislation"
					yield scrapy.Request(url=url, callback=self.parse, meta={"sorv":"v"})
					url = "https://www.whitehouse.gov/briefing-room/presidential-actions/executive-orders"
					yield scrapy.Request(url=url, callback=self.parse, meta={"sorv":"e"})
					url = "https://www.whitehouse.gov/briefing-room/presidential-actions/presidential-memoranda"
					yield scrapy.Request(url=url, callback=self.parse, meta={"sorv":"p"})

				def parse (self, response):

					sorv = response.meta.get('sorv')

					soup = BeautifulSoup(response.body, 'html.parser')
					panel = soup.find("div", {"class":"view-content"})
					if (panel == None):
						return
					bill = panel.find("div", {"class":"views-row views-row-1 views-row-odd views-row-first"})
					if (bill == None):
						bill = panel.find("div", {"class":"views-row views-row-1 view-row-even views-row-first"})
						if (bill == None):
							return
					date = time.strftime("%d/%m/%Y")
								
					name = bill.a.text
					link = "https://www.whitehouse.gov" + bill.a['href']


					if (self.bills.find_one({"name": name}) != None):
						print("Found entry in DB")
						return

					bill = {'name': name, 'date': date, 'url' : link, 'status': sorv}
					self.bills.insert(bill)

					if (len(name) > 91):
						name = name[0:88]
						name = name + "..."
					
					if (sorv == "s"):         
						to_tweet = "Donald Trump has signed: " + name + link
					elif (sorv == "e"):
						to_tweet = "Donald Trump has issued: " + name + link
					elif (sorv == "p"):
						to_tweet = "Donald Trump has issued: " + name + link
					else:
						to_tweet = "Donald Trump has vetoed: " + name +link

					print("\n\n\nDate: " + date + " To tweet: " + to_tweet + "\n\n\n")
					a = auth()

					try:
						api = twitter.Api(a.consumer_key, a.consumer_secret, a.access_token_key, a.access_token_secret)
						status = api.PostUpdate(to_tweet)
						print(status.text)
					except:
						return

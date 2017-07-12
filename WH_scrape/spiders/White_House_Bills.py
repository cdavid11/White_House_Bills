from __future__ import unicode_literals
import scrapy
from bs4 import BeautifulSoup
from pymongo import MongoClient
import twitter
from auth import auth


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

                def parse (self, response):

                    sorv = response.meta.get('sorv')
                    print("SORV: " + sorv)

                    soup = BeautifulSoup(response.body, 'html.parser')
                    panel = soup.find("div", {"class":"view-content"})
                    if (panel == None):
                        print("Nothing here")
                        return
                    bill = panel.find("div", {"class":"views-row views-row-1 views-row-odd views-row-first"})

                                
                    name = bill.a.text
                    link = "https://www.whitehouse.gov" + bill.a['href']
                    print(name)
                    print(link)


                    if (len(name) > 91):
                        diff = len(name) - 91
                        name = name[0:diff-3]
                        name = name + "..."
                    
                    if (sorv == "s"):         
                        to_tweet = "@POTUS has signed: " + name +link + "\n#Trump"
                    else:
                        to_tweet = "@POTUS has vetoed: " + name +link + "\n#Trump"
                    a = auth()

                    try:
                        api = twitter.Api(a.consumer_key, a.consumer_secret, a.access_token_key, a.access_token_secret)
                        status = api.PostUpdate(to_tweet)
                        print(status.text)
                    except:
                        print("Tweeting Error")
                        return
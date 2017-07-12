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
                link = "https://www.whitehouse.gov" + bill.a['href']
                print(name)
                print(link)


                if (len(name) > 91):
                        diff = len(name) - 91
                        name = name[0:diff-3]
                        name = name + "..."
               
                to_tweet = "@POTUS has signed: " + name +link + "\n#Trump"

                a = auth()

                print(len(to_tweet))


               	api = twitter.Api(a.consumer_key, a.consumer_secret, a.access_token_key, a.access_token_secret)
               	status = api.PostUpdate(to_tweet)
               	print(status.text)

#!/usr/bin/python
from __future__ import unicode_literals
import scrapy
from bs4 import BeautifulSoup
from pymongo import MongoClient
import twitter
from auth import auth
import time


class Old_Bill_Spider (scrapy.Spider):

                                name = "Get_Old_Bills"
                                connection = MongoClient()
                                db = connection['Bills']
                                bills = db.bills

                                def start_requests (self):

                                    i = 0
                                    while (i < 6):
                                            url = "https://www.whitehouse.gov/briefing-room/signed-legislation?field_legislation_status_value=0&page=" + str(i)
                                            i += 1
                                            time.sleep(1)
                                            yield scrapy.Request(url=url, callback=self.parse)

                                def parse (self, response):

                                        soup = BeautifulSoup(response.body, 'html.parser')
                                        panel = soup.find("div", {"class":"view-content"})
                                        if (panel == None):
                                            return
                                        the_bills = panel.find_all("h3", {"class":"field-content"})
                                        urls = panel.find_all("a")
                                        dates = panel.find_all("span",{"class":"date-display-single"})
                                        if (the_bills == None):
                                            return
                                        for bill in the_bills:
                                            print(bill.text.encode('utf-8'))
                                        for url in urls:
                                            print(url['href'])
                                        for date in dates:
                                            print(date['content'])

                                        i = 0
                                        while(i < 10):
                                            if(self.bills.find_one({"name":the_bills[i].text.encode('utf8')}) == None):
                                                bill = {'name': the_bills[i].text.encode('utf8'), 'date': dates[i]['content'], 'url' : "https://www.whitehouse.gov" +urls[i]['href'], 'status' : "s"}
                                                self.bills.insert(bill)
                                            i+=1
                                        #for bill in panel:
                                         #   date = bill.find_all("div",{"class":"field-content"})
                                          #  print(date)
                                            #date = bill.find("span", {"class":"date-display-single"})
                                            #print(date)                                  
                                           # name = bill['a'].text
                                            #link = "https://www.whitehouse.gov" + bill['a']

                                            #print(name)
                                            #print(link)
                                        #if (self.bills.find_one({"name": name}) != None):
                                        #    print("Found entry in DB")
            #return

                                        #bill = {'name': name, 'date': date, 'url' : link, 'status': sorv}
                                        #self.bills.insert(bill)

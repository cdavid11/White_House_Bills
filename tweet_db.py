#This is just a quick script that will tweet every single item in the database currently. It's a one off script
# that shouldn't need to be used again as the bot is run live.

import twitter
import pymongo
from auth import auth
import time

connection = pymongo.MongoClient()
db = connection['Bills']
bills = db.bills

a = auth()

all_bills = bills.find().sort('date', pymongo.ASCENDING)
for bill in all_bills:
	name = bill['name']
	url = bill['url']
	print(url)
	if (len(name) > 91):
		name = name[0:87]
		name = name + "... "
	to_tweet = "#DonaldTrump has signed: " + name + " " + url
	print(to_tweet)
	print("Length: " + str((len(to_tweet) - len(url) + 23)))

	api = twitter.Api(a.consumer_key, a.consumer_secret, a.access_token_key, a.access_token_secret)
	status = api.PostUpdate(to_tweet, verify_status_length = False)
	time.sleep(1)
	print(status.text)


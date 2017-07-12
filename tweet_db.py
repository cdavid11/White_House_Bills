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
	if (len(name) > 91):
		name = name[0:88]
		name = name + "..."
	to_tweet = "@POTUS has signed: " + name + url + "\n#Trump"
	print(to_tweet)
	print("Length: " + str((len(to_tweet) - len(url) + 23)))
	

	api = twitter.Api(a.consumer_key, a.consumer_secret, a.access_token_key, a.access_token_secret)
	status = api.PostUpdate(to_tweet)
	time.sleep(1)
	print(status.text)


import tweepy
import pymongo
from time import time, strftime, localtime, gmtime, sleep
from keys import API_KEY, API_KEY_SECRET, MONGODB_KEY


def wall_time_str(sec):
	if sec >= 3600:
		return strftime("%Hh%M'%S\"", gmtime(sec))
	else:
		return strftime("   %M'%S\"", gmtime(sec))

def local_time_str():
	return strftime('%H:%M:%S', localtime())

def log(file, query):
	with open(file, 'a') as f:
		f.write(strftime('%a, %d %b %Y %H:%M:%S', localtime()) + '\n')
		for k in query:
			f.write('{} = {}\n'.format(k.capitalize(), query[k]))
		f.write('\n\n')


def make_query(api, db, name, search, lang=None, since=None, until=None, max_id=None, items=0):

	# Create Collection
	col = db[name]

	c = 0
	since_runtime = time()
	print('Collecting tweets for query \"{}\"...'.format(name))

	cursor = tweepy.Cursor(api.search, q=search, lang=lang, since=since, until=until, max_id=max_id, tweet_mode='extended').items(items)

	while True:
		try:
			for tweet in cursor:

				json_data = tweet._json
				json_data['_id'] = json_data['id']
				try:
					col.insert_one(json_data)
				except pymongo.errors.DuplicateKeyError:
					print('Duplicated detected')
					break

				c += 1
				if c % 1000 == 0:
					t = time() - since_runtime
					print('{} --> Collected {:6d} tweets in {}'.format(local_time_str(), c, wall_time_str(t)))
			break
		except tweepy.error.TweepError as e:
			print('{} --> {}. Waiting 10 minutes.'.format(local_time_str(), e))
			sleep(600)
			continue

	print('Collected {} tweets in {} for query \"{}\".\n\n'.format(c, wall_time_str(time() - since_runtime), name))

######################################

# query https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/guides/standard-operators
# params https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets

if __name__ == '__main__':

	## SET PYMONGO ##
	client = pymongo.MongoClient('fpsds.synology.me', 27017, username='mongoadmin', password=MONGODB_KEY)
	db = client['tweets']

	## SET TWITTER DEV ##
	auth = tweepy.AppAuthHandler(API_KEY, API_KEY_SECRET)
	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

	queries = [
		{'name': '#covid_vaccine',
		'search': '#covid OR #covid19 vaccine OR vacuna',
		'lang': None,
		'since': None,
		'until': None,
		'max_id': None,
		'items': 0
		},
	]

	log_file = 'log.txt'

	for query in queries:
		log(log_file, query)
		make_query(api, db, **query)

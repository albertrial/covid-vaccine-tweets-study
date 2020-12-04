# import pprint
import tweepy
import pymongo
from time import time, strftime, localtime, gmtime
from keys import API_KEY, API_KEY_SECRET


def wall_time_str(sec):
	if sec >= 3600:
		return strftime("%Hh%M'%S\"", gmtime(sec))
	else:
		return strftime("   %M'%S\"", gmtime(sec))

def local_time_str():
	return strftime('%H:%M:%S', localtime())

def log(file, query):
	file.write(strftime('%a, %d %b %Y %H:%M:%S', localtime()) + '\n')
	file.write('Name = ' + query['name'] + '\n')
	file.write('Search = ' + query['search'] + '\n')
	file.write('Lang = ' + str(query['lang']) + '\n')
	file.write('Since = ' + str(query['since']) + '\n')
	file.write('Until = ' + str(query['until']) + '\n\n\n')


def make_query(api, db, query):

	# Create Collection
	col = db[query['name']]

	c = 0
	since = time()
	print('Collecting tweets for query \"{}\"...'.format(query['name']))

	for tweet in tweepy.Cursor(api.search, q=query['search'], lang=query['lang'], since=query['since'], until=query['until'], tweet_mode='extended').items():

		json_data = tweet._json
		json_data['_id'] = json_data['id']
		try:
			col.insert_one(json_data)
		except pymongo.errors.DuplicateKeyError:
			print('Duplicated detected')
			break

		c += 1
		if c % 1000 == 0:
			t = time() - since
			print('{} --> Collected {:6d} tweets in {}'.format(local_time_str(), c, wall_time_str(t)))

	print('Done collecting tweets for query {}.\n\n'.format(query['name']))

######################################

# query https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/guides/standard-operators
# params https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets

# + Una amb tots els llenguatges (#vaccine or #vacuna #....)
# + Un hashtag d'eleccions (Elections2020) a veure què passa
# + Una provant el filtre positiu de twitter
# + Una provant el filtre negatiu de twitter
# + Una query sense hashtag (sino vaccine directament)
# + Una query amb #COVID19
# - Una query amb #EndSARS


# query = ('Query_Name', 'Query_Search', 'lang', 'since', 'until')
# query = ('Vaccine_no_since', '#Vaccine', None, None, None)


if __name__ == '__main__':

	## SET PYMONGO ##
	client = pymongo.MongoClient('fpsds.synology.me', 27017, username='mongoadmin', password='bda')
	db = client['tweets']

	## SET TWITTER DEV ##
	auth = tweepy.AppAuthHandler(API_KEY, API_KEY_SECRET)
	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

	queries = [
		{'name': 'vaccine_langs',
		'search': '#Vaccine OR #Vacuna OR #Vaccin OR #Impfstoffe OR #Vaccino',
		'lang': None,
		'since': None,
		'until': None
		},
		{'name': 'elections2020_single',
		'search': '#Elections2020',
		'lang': 'en',
		'since': None,
		'until': None
		},
		{'name': 'vaccine_positive',
		'search': '#Vaccine :)',
		'lang': 'en',
		'since': None,
		'until': None
		},
		{'name': 'vaccine_negative',
		'search': '#Vaccine :(',
		'lang': 'en',
		'since': None,
		'until': None
		},
		{'name': 'vaccine_wo_hashtag',
		'search': 'vaccine',
		'lang': 'en',
		'since': None,
		'until': None
		},
		{'name': 'covid_no_lang',
		'search': '#COVID19',
		'lang': None,
		'since': None,
		'until': None
		},
	]

	log_file = open('log.txt', 'a')

	for query in queries:
		make_query(api, db, query)
		log(log_file, query)

	log_file.close()
import pymongo
from keys import MONGODB_KEY
import langid
import pickle

def get_tweet_text(tweet):
    if 'retweeted_status' in tweet:
        tweet = tweet['retweeted_status']
    
    return tweet['full_text']

client = pymongo.MongoClient('localhost', 27017, username='mongoadmin', password=MONGODB_KEY)
tweets = client['tweets']['#covid_vaccine']

twitter_lang = []
detected_lang = []
for i, tweet in enumerate(tweets.find({}, {'full_text':1, 'lang':1, 'retweeted_status.full_text':1})):
    twitter_lang.append(tweet['lang'])
    detected_lang.append(langid.classify(get_tweet_text(tweet))[0])

    if i % 5000 == 0:
    	print(i)

with open('lang_comp.pkl', 'wb') as f:
	pickle.dump({'twitter': twitter_lang, 'langid': detected_lang}, f)

from datetime import datetime
import pymongo
from keys import MONGODB_KEY

client = pymongo.MongoClient('fpsds.synology.me', 27017, username='mongoadmin', password=MONGODB_KEY)
db = client['tweets']
tweets = db['#covid_vaccine']

for tweet in tweets.find({'date': {'$exists': False}}, {'created_at':1}):
    # Parse formatted string
    dt = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')
    # Include new field with format YYYY-MM-DD
    tweets.update_one({'_id': tweet['_id']}, {'$set': {'date': dt.strftime('%Y-%m-%d')}})
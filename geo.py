import googlemaps
from keys import GOOGLE_API_KEY

import pymongo

# By default it has rate limit enabled 50 queries/s
# By default 1 minute retry for server errors
gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

## SET PYMONGO ##
client = pymongo.MongoClient('fpsds.synology.me', 27017, username='mongoadmin', password='bda')
tweets_col = client['tweets']['vaccine_top3_hashtags']
geo_col = client['geo']['locations']


locations = get_unique_locations(tweets_col)
for location in locations:
	geocode_result = gmaps.geocode(address=location)
	geo_col.insert_one({'_id': location, 'gmaps': geocode_result})







# https://googlemaps.github.io/google-maps-services-python/docs/index.html
# geocode_result = gmaps.geocode(address='location', bounds='NE and SW bounding box', language='en?')
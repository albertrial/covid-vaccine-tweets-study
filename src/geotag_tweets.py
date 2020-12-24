import re
import json
import pymongo
from collections import defaultdict
from keys import MONGODB_KEY


STATE_RE = re.compile(r'(.+),\s*(\w+)')								# Find Structures such Alaior, Menorca
WHITES_RE = re.compile(r'\s+')										# Find whitespaces, tabs and newlines
PUNCTUATION_RE = re.compile(r'\W+')									# Find all punctuation signs
SEPARATORS_RE = re.compile(r'(?:(?: \-)|[/|\\\(\),])+')				# Find "important" separators --> Alaior, Menorca. Alaior - Menorca. Alaior/Menorca. Alaior|Menorca. Alaior\Menorca. Alaior (Menorca)
STRIPPING_RE = re.compile(r'^\W+|\W+$')								# Find non-alphanumeric characters at the start and end of string


def normalize(location_name):
	x = re.sub(WHITES_RE, ' ', location_name.lower())               # Collapse whitespaces, tabs and newlines into a single whitespaces
	x = re.sub(PUNCTUATION_RE, ' ', x)                              # Substitute all punctuation signs by whitespaces
	x = x.strip()                                                   # Remove extra whitespaces
	
	return x


def normalize_commas(location_name):
	x = re.sub(WHITES_RE, ' ', location_name.strip().lower())       # Collapse whitespaces, tabs and newlines into a single whitespaces
	x = re.sub(SEPARATORS_RE, 'a1b2c3d4e5', x)                      # Detect "important" separators, and replace them to a special token
	x = re.sub(PUNCTUATION_RE, ' ', x)                              # Substitute all the remaining punctuation signs by whitespaces
	x = re.sub(re.compile(r'\s*a1b2c3d4e5\s*'), ', ', x)            # Convert all the important separators to ', '
	x = re.sub(STRIPPING_RE, '', x)                                 # Remove extra whitespaces or ', '
	return x


def load_known_locations(filename):
	with open(filename, encoding='utf-8') as f:
		location_list = json.load(f)

	alias_location = {}
	location_dict = defaultdict(lambda: None)
	for location in location_list:
		location_dict[location['_id']] = location
		for alias in location['aliases']:
			alias_location[alias] = location['_id']

	return alias_location, location_dict


def resolve_tweet(tweet, force_coordinates=False):
	# Resolve by place
	place = tweet['place']
	if place:
		match = match_comma_structure(normalize_commas(place['full_name']))
		if not match:
			normalized_country = normalize(place['country'])
			if normalized_country in ALIAS_LOCATION:
				match = normalized_country
		if match:
			return ensure_coordinates(ALIAS_LOCATION[match], force_coordinates)

	# Resolve by user.location
	user_location = tweet['user']['location']
	if user_location:
		# Normalize without commas, just like the aliases
		normalized = normalize(user_location)

		# Exact normalized match
		if normalized in ALIAS_LOCATION:
			return ensure_coordinates(ALIAS_LOCATION[normalized], force_coordinates)

		# Try preserving commas and matching states
		match = match_comma_structure(normalize_commas(user_location))
		if match:
			return ensure_coordinates(ALIAS_LOCATION[match], force_coordinates)
	
	return None


def match_comma_structure(normalized_location):
	match = STATE_RE.search(normalized_location)
	provisional_match = None
	while match:
		before_comma = match.group(1)
		after_comma = match.group(2)
		
		if before_comma in ALIAS_LOCATION:
			provisional_match = before_comma
		elif after_comma in ALIAS_LOCATION:
			provisional_match = after_comma

		match = STATE_RE.search(before_comma)
	return provisional_match


def ensure_coordinates(_id, force_coordinates):
	if not force_coordinates:
		return _id
	while _id != '-1' and 'latitude' not in LOCATION_DICT[_id]:
		_id = LOCATION_DICT[_id]['parent_id']
	# Any parent has coordinates
	if _id == '-1':
		_id = None
	return _id


######################################################################
if __name__ == '__main__':
	client = pymongo.MongoClient('fpsds.synology.me', 27017, username='mongoadmin', password=MONGODB_KEY)
	tweets_col = client['tweets']['#covid_vaccine']

	ALIAS_LOCATION, LOCATION_DICT = load_known_locations('../data/cleaned_locations.json')

	tweets = tweets_col.find({'my_geo': {'$exists': False}}, {'user.location': 1, 'place': 1, 'geo': 1, 'coordinates': 1, '_id': 1})
	has_coordinates = count = total = 0
	for tweet in tweets:
		location = resolve_tweet(tweet, force_coordinates=True)
		if location:
			if 'latitude' in LOCATION_DICT[location]:
				has_coordinates += 1
			count += 1
		tweets_col.update_one({'_id': tweet['_id']}, {'$set': {'my_geo': LOCATION_DICT[location]}})
		total += 1
		if total % 5000 == 0:
			print('Processed {:6d} tweets'.format(total))

	# print(count, total, 100*count/total)
	# print(has_coordinates, total, 100*has_coordinates/total)
	print('Done. {} tweets were updated. {:.2f}% of them matched with a location.'.format(total, 100*count/total))

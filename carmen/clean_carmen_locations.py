import pymongo
import json
from carmenxu import normalize, normalize_commas
from collections import defaultdict


def insert_locations():
	## SET PYMONGO ##
	# client = pymongo.MongoClient('fpsds.synology.me', 27017, username='mongoadmin', password='bda')
	# geo_col = client['geo']['known_locations']

	# Open locations file
	with open('locations.json', encoding='utf-8') as f:
		lines = f.readlines()
	
	all_aliases = defaultdict(list)
	all_locations = {}

	for line in lines:
		location = json.loads(line)
		location['_id'] = location.pop('id')
		loc_id = location['_id']
		all_locations[loc_id] = location

		aliases = []
		if 'aliases' in location:
			aliases = location['aliases']
		
		processed_aliases = set()
		# Add normalizations
		for alias in aliases:
			if alias not in processed_aliases:
				processed_aliases.add(alias)
				processed_aliases.add(normalize(alias))
				processed_aliases.add(normalize_commas(alias))

		# Add countrycode
		if location['parent_id'] == '-1' and 'countrycode' in location:
			processed_aliases.add(location['countrycode'].lower())
		# Add statecode for USA locations
		if location['parent_id'] == '2645' and 'statecode' in location:
			processed_aliases.add(location['statecode'].lower())
		# Add city, county, state and country
		if location['city'] != '':
			processed_aliases.add(location['city'].lower())
		elif location['county'] != '':
			processed_aliases.add(location['county'].lower())
		elif location['state'] != '':
			processed_aliases.add(location['state'].lower())
		else:
			processed_aliases.add(location['country'].lower())

		for alias in processed_aliases:
			all_aliases[alias].append(loc_id)

	# Duplicate Processing
	for key in frozenset(all_aliases.keys()):
		if len(all_aliases[key]) == 1:
			all_aliases[key] = all_aliases[key][0]
		else:
			locs = all_aliases[key]
			provisional_cities = []
			provisional_counties = []
			provisional_states = []
			provisional_countries = []
			for loc in locs:
				if all_locations[loc]['city'] != '':
					provisional_cities.append(loc)
				elif all_locations[loc]['county'] != '':
					provisional_counties.append(loc)
				elif all_locations[loc]['state'] != '':
					provisional_states.append(loc)
				else:
					provisional_countries.append(loc)
			if len(provisional_cities) == 1:
				all_aliases[key] = provisional_cities[0]
			elif len(provisional_cities) > 1:
				del all_aliases[key]
			else:
				if len(provisional_counties) == 1:
					all_aliases[key] = provisional_counties[0]
				elif len(provisional_counties) > 1:
					del all_aliases[key]
				else:
					if len(provisional_states) == 1:
						all_aliases[key] = provisional_states[0]
					elif len(provisional_states) > 1:
						del all_aliases[key]
					else:
						if len(provisional_counties) == 1:
							all_aliases[key] = provisional_counties[0]
						else:
							del all_aliases[key]


	# Compute final list of aliases for each location
	location_aliases = defaultdict(list)
	for alias in all_aliases.keys():
		location_aliases[all_aliases[alias]].append(alias)

	json_list = []
	# Update aliases list and insert to db
	for loc_id in all_locations:
		loc = all_locations[loc_id]
		loc['aliases'] = location_aliases[loc_id]
		json_list.append(loc)
		# geo_col.insert_one(loc)
		# try:
		# 	geo_col.insert_one(location)
		# except pymongo.errors.DuplicateKeyError:
		# 	continue

	with open('cleaned_locations.json', 'w', encoding='utf-8') as f:
		json.dump(json_list, f, indent=2)

	print('{} locations added to the database'.format(len(location_aliases)))


if __name__ == '__main__':
	insert_locations()
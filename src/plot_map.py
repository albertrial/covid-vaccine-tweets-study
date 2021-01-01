import pymongo
import json
import folium
import branca.colormap as cmp
from folium.plugins import MarkerCluster # for clustering the markers
import numpy as np
from collections import defaultdict


## SET PYMONGO ##
client = pymongo.MongoClient('fpsds.synology.me', 27017, username='mongoadmin', password='bda')
tweets = client['tweets']['#covid_vaccine']

# pip = [
# 	{'$match': {'my_geo': {'$ne': None}}},
# 	{'$group': {'_id': '$my_geo.country', 'counts': {'$sum': 1}}},
# ]
# countries_with_tweets = tweets.aggregate(pip)
# countries = {e['_id']: e['counts'] for e in countries_with_tweets}
# # print(sorted(list(countries.values())))
# # bins = list(np.quantile(list(countries.values()), [0, 0.2, 0.4, 0.6, 0.8, 1]))

# m = folium.Map()
# folium.Choropleth(geo_data='../data/world-countries.json',
# 	name='Tweet Counts',
# 	data=countries,
# 	key_on='feature.properties.name',
# 	bins=[0, 500, 1000, 5000, 20000, 50000, 250000],
# 	legend_name='Tweet count').add_to(m)
# folium.LayerControl().add_to(m)

# m.save('a.html')

###################################################################################################################
# map = folium.Map()

# # Add a marker for every record in the data, use a clustered view
# marker_cluster = MarkerCluster().add_to(map) # create marker clusters

# client = pymongo.MongoClient('localhost', 27017, username='mongoadmin', password='bda')
# tweets = client['tweets']['#covid_vaccine']
# for tw in tweets.find({'my_geo': {'$ne': None}}, {'_id':0, 'my_geo':1}):
#     location = [tw['my_geo']['latitude'],tw['my_geo']['longitude']]
#     folium.Marker(location).add_to(marker_cluster)
    
# map.save('b.html')
###################################################################################################################

# pip = [
# 	{'$match': {'my_geo.country': 'United States'}},
# 	{'$group': {'_id': '$my_geo.statecode', 'counts': {'$sum': 1}}},
# ]
# countries_with_tweets = tweets.aggregate(pip)
# countries = {e['_id']: e['counts'] for e in countries_with_tweets}
# # print(sorted(list(countries.values())))



# m = folium.Map(location=[37, -102], zoom_start=5)
# folium.Choropleth(geo_data='../data/us-states.json',
# 	name='Tweet Counts',
# 	data=countries,
# 	key_on='feature.id',
# 	# fill_color='RdYlGn',
# 	# fill_color='BuPu',
# 	fill_color='YlOrBr',
# 	bins=[0, 1000, 2500, 5000, 10000, 15000, 20000, 35000],
# 	legend_name='Tweet count').add_to(m)
# folium.LayerControl().add_to(m)

# m.save('c.html')


# ###################################################################################################################
# pip = [
# 	{'$match': {'my_geo.country': 'United States', 'vaccine_acceptance.global_acceptance': {'$ne': 'neutral'}}},
# 	{'$group': {'_id': {'state': '$my_geo.statecode', 'acceptance': '$vaccine_acceptance.global_acceptance'}, 'count': {'$sum':1}}},
# 	{'$group': {'_id': '$_id.state', 'count_group': {'$push': {'acceptance': '$_id.acceptance', 'count': '$count'}}}}
# ]

# res = tweets.aggregate(pip)
# states = {state['_id']: defaultdict(int, {group['acceptance']: group['count'] for group in state['count_group']}) for state in res}
# # print(states)
# states_acceptance = {state: states[state]['in_favour']/(states[state]['in_favour'] + states[state]['against']) for state in states}
# # print(sorted(list(countries.values())))



# m = folium.Map(location=[37, -102], zoom_start=5)
# folium.Choropleth(geo_data='../data/us-states.json',
# 	name='Vaccine Acceptance',
# 	data=states_acceptance,
# 	key_on='feature.id',
# 	fill_color='RdYlGn',
# 	# fill_color='BuPu',
# 	# fill_color='YlOrBr',
# 	bins=[0, 0.25, 0.5, 0.75, 1],
# 	legend_name='Vaccine Acceptance').add_to(m)
# folium.LayerControl().add_to(m)

# m.save('d.html')

###################################################################################################################
# pip = [
# 	{'$match': {'my_geo': {'$ne': None}, 'vaccine_acceptance.hashtag_acceptance': {'$ne': 'neutral'}, 'vaccines': 'Sputnik-V'}},
# 	{'$group': {'_id': {'country': '$my_geo.country', 'acceptance': '$vaccine_acceptance.global_acceptance'}, 'count': {'$sum':1}}},
# 	{'$group': {'_id': '$_id.country', 'count_group': {'$push': {'acceptance': '$_id.acceptance', 'count': '$count'}}}}
# ]

# res = tweets.aggregate(pip)
# countries = {country['_id']: defaultdict(int, {group['acceptance']: group['count'] for group in country['count_group']}) for country in res}
# # print(states)
# countries_acceptance = {country: countries[country]['in_favour']/(countries[country]['in_favour'] + countries[country]['against']) for country in countries}
# # print(sorted(list(countries.values())))



# m = folium.Map()
# folium.Choropleth(geo_data='../data/world-countries.json',
# 	name='Vaccine Acceptance',
# 	data=countries_acceptance,
# 	key_on='feature.properties.name',
# 	fill_color='RdYlGn',
# 	# fill_color='BuPu',
# 	# fill_color='YlOrBr',
# 	bins=[0, 0.25, 0.5, 0.75, 1],
# 	legend_name='Vaccine Acceptance').add_to(m)
# folium.LayerControl().add_to(m)

# m.save('e.html')


# def map(data, region='world, states', type:'accept, count', save=filenameNone):
# 	m.save(filename+'.html')
# 	return m


###################################################################################################################


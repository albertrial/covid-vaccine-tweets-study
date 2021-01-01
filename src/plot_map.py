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
# import numpy as np
# import matplotlib.pyplot as plt
# def stacked_barplot(x_ticks, y, title='', x_label='', y_label='', label_rotation=0, figsize=(6.4, 4.8)):
# 	y_pos = np.arange(len(x_ticks))
	 
# 	plt.figure(figsize=figsize)

# 	# Create bars
# 	plt.bar(y_pos, y, color='mediumspringgreen', edgecolor='white')
# 	plt.bar(y_pos, [1-e for e in y], bottom=y, color='lightcoral', edgecolor='white')
	 
# 	# Create names on the x-axis
# 	plt.xticks(y_pos, x_ticks, rotation=label_rotation)
# 	if label_rotation != 0:
# 		plt.subplots_adjust(bottom=0.4, top=0.99)
	 
# 	plt.title(title)
# 	plt.xlabel(x_label)
# 	plt.ylabel(y_label)
# 	# Show graphic
# 	plt.show()


# pip = [
# 	{'$match': {'vaccine_acceptance.hashtag_acceptance': {'$ne': 'neutral'}}}, # Filtrar per vaccines exist
# 	{'$unwind': '$vaccines'},
# 	{'$group': {'_id': {'vaccine': '$vaccines', 'acceptance': '$vaccine_acceptance.hashtag_acceptance'}, 'count': {'$sum':1}}},
# 	{'$group': {'_id': '$_id.vaccine', 'count_group': {'$push': {'acceptance': '$_id.acceptance', 'count': '$count'}}}}
# ]

# res = tweets.aggregate(pip)
# vaccines = {vaccine['_id']: defaultdict(int, {group['acceptance']: group['count'] for group in vaccine['count_group']}) for vaccine in res if vaccine['_id'] in ['Pfizer-BioNTech', 'Moderna', 'Oxford-AstraZeneca', 'Sputnik-V']}
# # print(states)
# vacciness = [vaccine for vaccine in vaccines]
# acceptance = [vaccines[vaccine]['in_favour']/(vaccines[vaccine]['in_favour'] + vaccines[vaccine]['against']) for vaccine in vaccines]
# # vaccine_acceptance = {vaccine: vaccines[vaccine]['in_favour']/(vaccines[vaccine]['in_favour'] + vaccines[vaccine]['against']) for vaccine in vaccines}
# # print(sorted(list(countries.values())))

# stacked_barplot(vacciness, acceptance, title='', x_label='', y_label='', label_rotation=90, figsize=(6, 8))

###################################################################################################################
import numpy as np
import matplotlib.pyplot as plt
from bson.son import SON
 
# def multi_barplot(x_ticks, y, y_labels, title='', x_label='', y_label='', label_rotation=0, figsize=(6.4, 4.8)):
# 	"""
# 	x = [A, B, C, D]
# 	y = [[a1, a2, a3, ...], [b1, b2, b3, ...], ...]
# 	"""

# 	# width of the bars
# 	offset = 0.05
# 	barWidth = 1/4 - offset
# 	skip = 1/5
	 
# 	# The x position of bars
# 	r0 = np.arange(len(x_ticks))
# 	rl = [x + 0.5 for x in r0]
# 	r1 = [x + skip for x in r0]
# 	r2 = [x + 2*skip for x in r0]
# 	r3 = [x + 3*skip for x in r0]
# 	r4 = [x + 4*skip for x in r0]

# 	y = np.array(y)	
# 	# Create blue bars
# 	plt.bar(r1, y[:, 0], width = barWidth, label=y_labels[0])
# 	plt.bar(r2, y[:, 1], width = barWidth, label=y_labels[1])
# 	plt.bar(r3, y[:, 2], width = barWidth, label=y_labels[2])
# 	plt.bar(r4, y[:, 3], width = barWidth, label=y_labels[3])
	 
# 	# general layout
# 	plt.xticks(rl, x_ticks, rotation=label_rotation)
# 	if label_rotation != 0:
# 		plt.subplots_adjust(bottom=0.4, top=0.99)
	 
# 	plt.title(title)
# 	plt.xlabel(x_label)
# 	plt.ylabel(y_label)
# 	plt.legend()

# 	# Show graphic
# 	plt.show()

# pip = [
# 	{'$match': {'vaccines': {'$exists': True}, 'my_geo': {'$ne': None}}},
# 	{'$group': {'_id': '$my_geo.country', 'count': {'$sum':1}}},
# 	{'$sort': SON([('count', pymongo.DESCENDING)])},
# 	{'$limit': 10}
# ]

# countries = tweets.aggregate(pip)
# countries = [e['_id'] for e in countries]

# pip = [
# 	{'$match': {'vaccines': {'$exists': True}, 'my_geo.country': {'$in': countries}}},
# 	{'$unwind': '$vaccines'},
# 	{'$group': {'_id': {'vaccine': '$vaccines', 'country': '$my_geo.country'}, 'count': {'$sum':1}}},
# 	{'$group': {'_id': '$_id.country', 'count_group': {'$push': {'vaccine': '$_id.vaccine', 'count': '$count'}}}}
# ]

# res = tweets.aggregate(pip)

# countries = []
# counts = []
# vaccines = ['Pfizer-BioNTech', 'Moderna', 'Oxford-AstraZeneca', 'Sputnik-V']
# for r in res:
# 	countries.append(r['_id'])
# 	country_counts = [0, 0, 0, 0]
# 	for d in r['count_group']:
# 		if d['vaccine'] in vaccines:
# 			country_counts[vaccines.index(d['vaccine'])] = d['count']
# 	normalized = [e/sum(country_counts) for e in country_counts]
# 	counts.append(normalized)

# print(countries)
# print(counts)
# multi_barplot(countries, counts, vaccines, label_rotation=90)




def timeseries(x, y, labels, title='', x_label='', y_label='', label_rotation=0, figsize=(6.4, 4.8)):
	"""
	y = [[a1,a2,a3,a4,a5, ...], [b1,b2,b3,b4,b5, ...]]
	"""

	plt.figure(figsize=figsize)

	xs = set()
	# multiple line plot
	for i in range(len(y)):
		xs = xs.union(set(x[i]))
		# plt.plot(x, y, marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
		plt.plot(x[i], y[i], marker='o', markersize=4, linewidth=2, label=labels[i])

	plt.xticks(sorted(xs), sorted(xs), rotation=label_rotation)
	if label_rotation != 0:
		plt.subplots_adjust(bottom=0.4, top=0.99)
	 
	plt.title(title)
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	plt.ylim(0, 1)
	plt.legend()
	plt.show()

def timeseries2(x, y, labels, title='', x_label='', y_label='', label_rotation=0, figsize=(6.4, 4.8)):
	"""
	y = [[a1,a2,a3,a4,a5, ...], [b1,b2,b3,b4,b5, ...]]
	"""

	f, ax = plt.subplots(5, 1, sharex='col', figsize=figsize)

	# Calculate xs
	xs = set()
	for t in x:
		xs = xs.union(set(t))
	xs = sorted(xs)
	plt.xticks(range(len(xs)), xs, rotation=label_rotation)

	# multiple line plot
	for i in range(len(y)):
		xx = [xs.index(t) for t in x[i]]
		ax[i].plot(xx, y[i], marker='o', markersize=4, linewidth=2, label=labels[i])
		ax[i].set_ylim(0, 1)
		ax[i].set_title(labels[i])

	
	if label_rotation != 0:
		plt.subplots_adjust(bottom=0.4, top=0.99)
	 
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	f.tight_layout()

	plt.show()



pip = [
	{'$match': {'vaccine_acceptance.global_acceptance': {'$ne': 'neutral'}}},
	{'$group': {'_id': {'date': '$date', 'acceptance': '$vaccine_acceptance.global_acceptance'}, 'count': {'$sum':1}}},
	{'$group': {'_id': '$_id.date', 'count_group': {'$push': {'acceptance': '$_id.acceptance', 'count': '$count'}}}},
	{'$sort': SON([('_id', pymongo.ASCENDING)])}
]

res = tweets.aggregate(pip)

g_days = []
g_acceptances = []
for r in res:
	g_days.append(r['_id'])
	d = defaultdict(int, {group['acceptance']: group['count'] for group in r['count_group']})
	acceptance = d['in_favour']/(d['in_favour'] + d['against'])
	g_acceptances.append(acceptance)

# timeseries([days], [acceptances], ['test'], label_rotation=90)

pip = [
	{'$match': {'vaccine_acceptance.global_acceptance': {'$ne': 'neutral'}, 'vaccines': {'$exists': True}}},
	{'$unwind': '$vaccines'},
	{'$group': {'_id': {'date': '$date', 'acceptance': '$vaccine_acceptance.global_acceptance', 'vaccine': '$vaccines'}, 'count': {'$sum':1}}},
	{'$group': {'_id': {'date': '$_id.date', 'vaccine': '$_id.vaccine'}, 'count_group': {'$push': {'acceptance': '$_id.acceptance', 'count': '$count'}}}},
	{'$sort': SON([('_id.date', pymongo.ASCENDING)])}
]

res = tweets.aggregate(pip)

days = defaultdict(list)
acceptances = defaultdict(list)
vaccines = ['Pfizer-BioNTech', 'Moderna', 'Oxford-AstraZeneca', 'Sputnik-V']
for r in res:
	days[r['_id']['vaccine']].append(r['_id']['date'])
	d = defaultdict(int, {group['acceptance']: group['count'] for group in r['count_group']})
	acceptance = d['in_favour']/(d['in_favour'] + d['against'])
	acceptances[r['_id']['vaccine']].append(acceptance)
acceptances = [acceptances[vac] for vac in vaccines]
days = [days[vac] for vac in vaccines]

timeseries2(days + [g_days], acceptances + [g_acceptances], vaccines + ['Global'], label_rotation=90)

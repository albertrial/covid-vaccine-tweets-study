import os
import folium
import numpy as np
import matplotlib.pyplot as plt
from folium.plugins import MarkerCluster


def barplot(x_ticks, y, title='', x_label='', y_label='', label_rotation=0, figsize=(6.4, 4.8)):
    y_pos = np.arange(len(x_ticks))

    plt.figure(figsize=figsize)

    # Create bars
    plt.bar(y_pos, y)

    # Create names on the x-axis
    plt.xticks(y_pos, x_ticks, rotation=label_rotation)
    if label_rotation != 0:
        plt.subplots_adjust(bottom=0.4, top=0.99)

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    # Show graphic
    plt.show()


def stacked_barplot(x_ticks, y, title='', x_label='', y_label='', label_rotation=0, figsize=(6.4, 4.8)):
    y_pos = np.arange(len(x_ticks))

    plt.figure(figsize=figsize)

    # Create bars
    plt.bar(y_pos, y, color='mediumspringgreen', edgecolor='white')
    plt.bar(y_pos, [1 - e for e in y], bottom=y, color='lightcoral', edgecolor='white')

    # Create names on the x-axis
    plt.xticks(y_pos, x_ticks, rotation=label_rotation)
    if label_rotation != 0:
        plt.subplots_adjust(bottom=0.4, top=0.99)

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    # Show graphic
    plt.show()


def multi_barplot(x_ticks, y, y_labels, title='', x_label='', y_label='', label_rotation=0, figsize=(6.4, 4.8)):
    """
    x = [A, B, C, D]
    y = [[a1, a2, a3, ...], [b1, b2, b3, ...], ...]
    """

    # width of the bars
    offset = 0.05
    barWidth = 1 / 4 - offset
    skip = 1 / 5

    # The x position of bars
    r0 = np.arange(len(x_ticks))
    rl = [x + 0.5 for x in r0]
    r1 = [x + skip for x in r0]
    r2 = [x + 2 * skip for x in r0]
    r3 = [x + 3 * skip for x in r0]
    r4 = [x + 4 * skip for x in r0]

    y = np.array(y)

    plt.figure(figsize=figsize)

    # Create blue bars
    plt.bar(r1, y[:, 0], width=barWidth, label=y_labels[0])
    plt.bar(r2, y[:, 1], width=barWidth, label=y_labels[1])
    plt.bar(r3, y[:, 2], width=barWidth, label=y_labels[2])
    plt.bar(r4, y[:, 3], width=barWidth, label=y_labels[3])

    # general layout
    plt.xticks(rl, x_ticks, rotation=label_rotation)
    if label_rotation != 0:
        plt.subplots_adjust(bottom=0.4, top=0.99)

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()

    # Show graphic
    plt.show()


def map_choropleth(data, name, region='world', type='nb_tweets', save_filename=None):
    if region == 'world':
        m = folium.Map()
        geo_data = os.path.join('data', 'world-countries.json')
        key_on = 'feature.properties.name'
        if type == 'nb_tweets':
            bins = [0, 500, 1000, 5000, 20000, 50000, 250000]
    elif region == 'us':
        m = folium.Map(location=[37, -102], zoom_start=4)
        geo_data = os.path.join('data', 'us-states.json')
        key_on = 'feature.id'
        if type == 'nb_tweets':
            bins = [0, 1000, 2500, 5000, 10000, 15000, 20000, 35000]
    else:
        raise NotImplementedError()

    if type == 'nb_tweets':
        fill_color = 'YlOrBr'
        legend_name = 'Tweet count'
    elif type == 'acceptance':
        bins = [0, 0.25, 0.5, 0.75, 1]
        fill_color = 'RdYlGn'
        legend_name = 'Vaccine acceptance ratio'
    else:
        raise NotImplementedError()

    folium.Choropleth(geo_data=geo_data,
                      name=name,
                      data=data,
                      key_on=key_on,
                      fill_color=fill_color,
                      bins=bins,
                      legend_name=legend_name).add_to(m)

    folium.LayerControl().add_to(m)
    if save_filename is not None:
        m.save(save_filename + '.html')
    return m

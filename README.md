# Covid Vaccine Tweets Study

This work is the final project for the Big Data Analysis (BDA) course of the [Master in Artificial Intelligence (MAI)][mai] of the [Universitat Politècnica de Catalunya (UPC), BarcelonaTECH][upc].

In this project, we have collected almost 1M tweets talking about the Covid Vaccine, stored them in a [MongoDB][mongodb] database and analyzed them to extract relevant information. 

All this study is reported in the main file [`covid-vaccine-tweets-study.ipynb`][notebook], a self-contained notebook that introduces the problem, presents the followed methodology, and shows the results in a graphical way.<sup>1</sup>

The notebook contains interactive maps that cannot be rendered using GitHub's visualizer. However, it can still be visualized online, without any additional requirement, using Jupyter's nbviewer at [nbviewer/covid-vaccine-tweets-study.ipynb][nbviewer].

## Dependencies
This project was developed using [Python][python] 3.7 and we used [Jupyter][jupyter] to create the main notebook.

Additionally, we have used:

- [PyMongo][pymongo]. A MongoDB interface for Python.
- [Tweepy][tweepy]. A Twitter API interface for Python.

- [langid][langid]. A Language Identification tool. Used for the tweet language assessment.

- [TextBlob][textblob]. An NLP library that uses ML techniques for Tokenization, POS tagging, Spelling correction, ... Used for Sentiment Analysis specifically.
- [flair][flair]. An NLP library that uses state-of-the-art transformer models for several NLP tasks. Used for Sentiment Analysis too.

- [Matplotlib][mpl]. A visualization library for Python. Used to create the plots.
- [Folium][folium]. A visualization library for Python. Used to generate interactive maps.


#
<sup>1</sup> The gathered data is not available anymore. Therefore, the notebook serves as a report and cannot be executed again. Yet, all the code is functional and could be used for a similar project.

[python]: https://www.python.org/
[jupyter]: https://jupyter.org/
[pymongo]: https://pymongo.readthedocs.io/en/stable/
[mongodb]: https://www.mongodb.com/
[tweepy]: https://www.tweepy.org/
[langid]: https://github.com/saffsd/langid.py
[folium]: https://python-visualization.github.io/folium/
[mpl]: https://matplotlib.org/
[textblob]: https://textblob.readthedocs.io/en/dev/
[flair]: https://github.com/flairNLP/flair
[mai]: https://www.fib.upc.edu/en/studies/masters/master-artificial-intelligence
[upc]: https://www.upc.edu/en
[notebook]: covid-vaccine-tweets-study.ipynb
[nbviewer]: https://nbviewer.jupyter.org/github/albertrial/covid-vaccine-tweets-study/blob/master/covid-vaccine-tweets-study.ipynb





import re
import pymongo
from src.keys import MONGODB_KEY
from textblob import TextBlob
from flair.models import TextClassifier
from flair.data import Sentence

flair_classifier = TextClassifier.load('en-sentiment')

hashtags_in_favour = [
    'healthcarehero',
    'vaccinessavelives',
    'endcovideverywhere',
    'vacunauniversalygratuita',
    'vaccinesafety',
    'getvaccinated',
    'yosegurosí',
    'vaccineswork',
    'yomevacuno',
    'pfizerproud',
    'endcovidforall',
    'peoplesvaccine',
    'igottheshot',
    'thisisourshot'
]

hashtags_against = [
    'plandemia',
    'plandemic',
    'vaccineskill',
    'vaccineinjury',
    'vaccinedamage',
    'covidhoax',
    'medicalfraud',
    'pharmaceuticalskill',
    'yonomevacuno'
]


def clean_text(text):
    return re.sub(r"(@)|([^0-9A-Za-z.,¡!¿?:;%$€ \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text)


def get_tweet_text(tweet):
    tw = tweet
    if 'retweeted_status' in tweet:
        tw = tweet['retweeted_status']

    return tw['full_text']


def get_tweet_hashtags(tweet):
    tw = tweet
    if 'retweeted_status' in tweet:
        tw = tweet['retweeted_status']

    return tw['entities']['hashtags']


def get_tweet_sentiment(text):
    textblob_analysis = TextBlob(text)
    textblob_sentiment = textblob_analysis.sentiment.polarity
    textblob_subjectivity = textblob_analysis.sentiment.subjectivity

    flair_sentence = Sentence(text)
    flair_classifier.predict(flair_sentence)
    flair_sentiment = flair_sentence.labels[0].value
    flair_prob = flair_sentence.labels[0].score

    if textblob_sentiment > 0 and flair_sentiment == 'POSITIVE' and flair_prob >= 0.9 and textblob_subjectivity >= 0.35:
        sentiment = 'positive'
    elif textblob_sentiment < 0 and flair_sentiment == 'NEGATIVE' and flair_prob >= 0.9 and textblob_subjectivity >= 0.35:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'

    return sentiment


def get_hashtag_acceptance(hashtags):
    for hashtag in hashtags:
        if hashtag['text'].lower() in hashtags_in_favour:
            return 'in_favour'
        if hashtag['text'].lower() in hashtags_against:
            return 'against'
    return 'neutral'


def get_vaccine_acceptance(hashtag_acceptance, text_sentiment):
    vaccine_acceptance = {'hashtag_acceptance': hashtag_acceptance,
                          'text_sentiment': text_sentiment}

    if hashtag_acceptance == 'neutral':
        if text_sentiment == 'positive':
            vaccine_acceptance['global_acceptance'] = 'in_favour'
        elif text_sentiment == 'negative':
            vaccine_acceptance['global_acceptance'] = 'against'
        else:
            vaccine_acceptance['global_acceptance'] = 'neutral'
    else:
        vaccine_acceptance['global_acceptance'] = hashtag_acceptance

    return vaccine_acceptance


######################################################################
if __name__ == '__main__':
    client = pymongo.MongoClient('fpsds.synology.me', 27017, username='mongoadmin', password=MONGODB_KEY)
    db = client['tweets']
    tweets = db['#covid_vaccine']

    count_en = total = 0

    for tw in tweets.find({},
                          {'_id': 1, 'full_text': 1, 'entities.hashtags': 1, 'lang': 1,
                           'retweeted_status.full_text': 1, 'retweeted_status.entities.hashtags': 1,
                           'quoted_status.full_text': 1, 'quoted_status.entities.hashtags': 1}):

        hashtag_acceptance = get_hashtag_acceptance(get_tweet_hashtags(tw))
        text_sentiment = 'neutral'

        if tw['lang'] == 'en':
            text_sentiment = get_tweet_sentiment(clean_text(get_tweet_text(tw)))
            count_en += 1

        vaccine_acceptance = get_vaccine_acceptance(hashtag_acceptance, text_sentiment)
        tweets.update_one({'_id': tw['_id']}, {'$set': {'vaccine_acceptance': vaccine_acceptance}})

        if total % 5000 == 0:
            print('Processed {:6d} tweets'.format(total))

        total += 1

    print('Done. {} tweets were updated. {:.2f}% of them in english.'.format(total, 100 * count_en / total))

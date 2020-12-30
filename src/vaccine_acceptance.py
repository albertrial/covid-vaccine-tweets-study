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
    if 'retweeted_status' in tweet:
        return tweet['retweeted_status']['entities']['hashtags']

    elif 'quoted_status' in tweet:
        return tweet['entities']['hashtags'] + tw['quoted_status']['entities']['hashtags']

    else:
        return tweet['entities']['hashtags']


def get_tweet_sentiment(text):
    textblob_analysis = TextBlob(text)
    textblob_sentiment = textblob_analysis.sentiment.polarity
    textblob_subjectivity = textblob_analysis.sentiment.subjectivity

    flair_sentence = Sentence(text)
    flair_classifier.predict(flair_sentence)
    flair_sentiment = flair_sentence.labels[0].value
    flair_prob = flair_sentence.labels[0].score

    if textblob_sentiment >= 0.25 and flair_sentiment == 'POSITIVE' and flair_prob >= 0.9 and textblob_subjectivity >= 0.4:
        sentiment = 'positive'
    elif textblob_sentiment <= -0.15 and flair_sentiment == 'NEGATIVE' and flair_prob >= 0.9 and textblob_subjectivity >= 0.4:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'

    return sentiment  # , textblob_sentiment, flair_sentiment, flair_prob, textblob_subjectivity


def get_hashtag_acceptance(hashtags):
    for hashtag in hashtags:
        if hashtag['text'].lower() in hashtags_in_favour:
            return 'in_favour'
        if hashtag['text'].lower() in hashtags_against:
            return 'against'
    return 'neutral'


######################################################################
if __name__ == '__main__':
    client = pymongo.MongoClient('fpsds.synology.me', 27017, username='mongoadmin', password=MONGODB_KEY)
    db = client['tweets']
    tweets = db['#covid_vaccine']

    count_en = total = 0
    tweets_in_favour = {'positive': 0, 'negative': 0, 'neutral': 0}
    tweets_against = {'positive': 0, 'negative': 0, 'neutral': 0}
    tweets_neutral = {'positive': 0, 'negative': 0, 'neutral': 0}

    for tw in tweets.find({'hashtag_acceptance': {'$exists': False}},
                          {'_id': 1, 'full_text': 1, 'entities.hashtags': 1, 'lang': 1,
                           'retweeted_status.full_text': 1, 'retweeted_status.entities.hashtags': 1,
                           'quoted_status.full_text': 1, 'quoted_status.entities.hashtags': 1}):
        hashtag_acceptance = get_hashtag_acceptance(get_tweet_hashtags(tw))
        sentiment = 'neutral'

        if tw['lang'] == 'en':
            sentiment = get_tweet_sentiment(clean_text(get_tweet_text(tw)))

            if hashtag_acceptance == 'in_favour':
                tweets_in_favour[sentiment] += 1

            elif hashtag_acceptance == 'against':
                tweets_against[sentiment] += 1

            elif hashtag_acceptance == 'neutral':
                tweets_neutral[sentiment] += 1

            count_en += 1

        tweets.update_one({'_id': tw['_id']}, {'$set': {'hashtag_acceptance': hashtag_acceptance,
                                                        'text_sentiment': sentiment}})

        if total % 5000 == 0:
            print('Processed {:6d} tweets'.format(total))

        total += 1

    print("In favour", tweets_in_favour)
    print("Against", tweets_against)
    print("Neutral", tweets_neutral)

    print('Done. {} tweets were updated. {:.2f}% of them in english.'.format(total, 100 * count_en / total))

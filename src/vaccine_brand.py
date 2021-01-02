import re
import pymongo
from keys import MONGODB_KEY


def trim_tweet_text(text):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\/\/\S+)", " ", text).split())


def get_tweet_text(tweet):
    tw = tweet
    if 'retweeted_status' in tweet:
        tw = tweet['retweeted_status']

    return tw['full_text']


def get_vaccines(text):
    vaccines = []
    vaccine_matches = {
        'Pfizer-BioNTech': ['pfizer', 'biontech', 'comirnaty', 'tozinameran', 'bnt162b2'],
        'Moderna': ['moderna', 'mrna-1273'],
        'Oxford-AstraZeneca': ['astrazeneca', 'oxford', 'azd1222', 'covishield'],
        'Sputnik-V': ['sputnik', 'gamaleya', 'gam-covid-vac'],
        'CanSino': ['cansino', 'convidecia', 'ad5-ncov'],
        'Johnson & Johnson': ['johnson&johnson', 'johnson & johnson', 'j&j', 'janssen', 'ad26.cov2.s'],
        'EpiVacCorona': ['bektop', 'vector institute', 'epivaccorona', 'epivac '],
        'Novavax': ['novavax', 'nvx-cov2373'],
        'CureVac': ['curevac', 'cvncov'],
        'Sinopharm': ['sinopharm', 'bbibp-corv'],
        'AnGes': [' anges ', 'takara', 'ag0302-covid19', 'osaka university'],
        'Medicago-GSK': ['medicago'],
        'Sanofi-GSK': ['sanofi'],
        'Sinovac': ['sinovac', 'picovacc'],
        'Bharat Biotech': ['bharat ', 'bbv152'],
    }

    for vaccine in vaccine_matches:
        if any(match in text.lower() for match in vaccine_matches[vaccine]):
            vaccines.append(vaccine)

    return vaccines


######################################################################
if __name__ == '__main__':
    client = pymongo.MongoClient('fpsds.synology.me', 27017, username='mongoadmin', password=MONGODB_KEY)
    db = client['tweets']
    tweets = db['#covid_vaccine']

    count_vaccine = total = 0

    for tw in tweets.find({},{'_id': 1, 'full_text': 1, 'retweeted_status.full_text': 1}):

        vaccines = get_vaccines(trim_tweet_text(get_tweet_text(tw)))

        if len(vaccines) > 0:
            tweets.update_one({'_id': tw['_id']}, {'$set': {'vaccines': vaccines}})
            count_vaccine += 1

        if total % 5000 == 0:
            print('Processed {:6d} tweets'.format(total))

        total += 1

    print('Done. {} tweets were processed. {:.2f}% of them talking about a specific vaccine.'.format(total, 100 * count_vaccine / total))

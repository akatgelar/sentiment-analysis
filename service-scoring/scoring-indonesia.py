from SentimentIndonesia import SentimentAnalysisIndonesia
import requests
import json
import logging

s = SentimentAnalysisIndonesia(
    filename='SentiWordNet_3.0.0_20130122_Indonesia.txt', weighting='geometric')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='log/access.log',
                    filemode='a+')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logging.info('This is log \n')
logger1 = logging.getLogger('sentiment-analysis.service-translator')


def scoring(tweet):

    try:
        print(tweet)
        score = s.score(tweet)
    except Exception as e:
        logger1.error("Error get score")
        logger1.error(e)

    return score


def main():
    string1 = 'suka'
    print(string1)
    score1 = scoring(string1)
    print(score1)
    print()

    string2 = 'rusak'
    print(string2)
    score2 = scoring(string2)
    print(score2)
    print()

    string3 = 'sepertinya'
    print(string3)
    score3 = scoring(string3)
    print(score3)
    print()


if __name__ == '__main__':
    main()

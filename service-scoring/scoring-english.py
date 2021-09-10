from SentimentEnglish import SentimentAnalysisEnglish
from pymongo import MongoClient
from pprint import pprint
import requests
import json
import logging
import bson
import datetime 
from time import sleep
import gspread
from oauth2client.service_account import ServiceAccountCredentials

s = SentimentAnalysisEnglish(filename='SentiWordNet_3.0.0_20130122_English.txt', weighting='geometric')

dbclient = MongoClient("mongodb://localhost:27017/")
db = dbclient.SentimentAnalysis

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M', filename='log/access.log', filemode='a+')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logging.info('This is log \n')
logger1 = logging.getLogger('sentiment-analysis.service-translator')


def removing(text):
    
    text = text.split(" ")
    texts = ""
    for k in text:
        if "@"  in k:
            pass
        elif "http"  in k:
            pass
            pass
        elif "#"  in k:
            pass
        else:
            texts = texts + " " + k

    return texts

def translate(text, gc):
    # PARAMS["q"] = text 
    sleep(3)
    try:
        
        wks = gc.open("service-translator-sentiment-analysis").sheet1
        wks.update_acell('A2', '=gTranslate("'+text+'", "id", "en")')
        cell_list = wks.acell('A2').value

        return cell_list

    except Exception as e:
        raise Exception("Error POST to Google Translate")
        return ""

 
def scoring(text):
     
    try: 
        score = s.score(text)
        return score
    except Exception as e:
        logger1.error("Error get score")
        logger1.error(e)
        return None


def sentiment(point):
     
    if(float(point) <= -0.005):
        return "negatif"
    elif(-0.005 < float(point) < 0.005):
        return "netral"
    elif(float(point) >= 0.005):
        return "positif"
    else:
        return "none"

def main():

    try:

        # translate = requests.post(url=URL, params=PARAMS, headers=HEADERS, timeout=10)
        # response_translate = translate.json()
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)

        gc = gspread.authorize(credentials)

        # return cell_list

        result = db.tweets.find({"scoring_progress": False}).sort('_id', 1).limit(1000).skip(0)

        for res in result:

            id = res['id']
            print(id)

            text = str(res['text']) 
            text = text.replace("\"","'")
            print(text.replace("\n", " "))
            
            return_removing = removing(text) 
            print(return_removing.replace("\n", " "))

            return_translate = translate(return_removing, gc)
            print(return_translate.replace("\n", " "))

            if(return_translate == "#ERROR!"):
                raise Exception("Error translating")
            elif(return_translate == "#NAME?"):
                raise Exception("Error translating")
            else:
                return_scoring = scoring(return_translate)
                print(return_scoring)
            
                if(return_scoring == "-0.46875"):
                    raise Exception("Error translating, scoring fail")
                else:
                    return_sentiment = sentiment(return_scoring)
                    print(return_sentiment)

                    topics = db.topics.find({"type": res['search_by'], "value": res['search_value']}).sort('_id', 1).limit(1)

                    count_all = int(topics[0]['count_all'])
                    count_finish = int(topics[0]['count_finish'])
                    count_unfinish = int(topics[0]['count_unfinish'])
                    sentiment_positif = int(topics[0]['sentiment_positif'])
                    sentiment_negatif = int(topics[0]['sentiment_negatif'])
                    sentiment_netral = int(topics[0]['sentiment_netral'])

                    count_finish = count_finish + 1
                    count_unfinish = count_all-count_finish
                    if(return_sentiment == "positif"):
                        sentiment_positif = sentiment_positif + 1
                    if(return_sentiment == "negatif"):
                        sentiment_negatif = sentiment_negatif + 1
                    if(return_sentiment == "netral"):
                        sentiment_netral = sentiment_netral + 1
        
                    try: 
                        db.topics.update({"type": res['search_by'], "value": res['search_value']},
                        {"$set" : {
                            "count_finish": bson.int64.Int64(count_finish),
                            "count_unfinish": bson.int64.Int64(count_unfinish),
                            "sentiment_positif": bson.int64.Int64(sentiment_positif),
                            "sentiment_negatif": bson.int64.Int64(sentiment_negatif),
                            "sentiment_netral": bson.int64.Int64(sentiment_netral)  
                        }})
                    except Exception as e:
                        print(e)
                        pass


                    try: 
                        now = datetime.datetime.now()   
                        db.tweets.update({"_id": bson.ObjectId(res['_id'])},
                        {"$set" : {
                            "scoring_progress": True,
                            "scoring_progress_date": now,
                            "scoring_translate": return_translate,
                            "scoring_point": return_scoring,
                            "scoring_sentiment": return_sentiment
                        }})
                    except Exception as e:
                        print(e)
                        pass
            
            print()

            
            
            
    except Exception as e:
        print(e)
        pass
 
if __name__ == '__main__':
    main()

import config
import oauth2 as oauth
import json
import time
import requests
import datetime
import bson
from pymongo import MongoClient
from pprint import pprint

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_KEY = ""
ACCESS_SECRET = ""

consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)

client = oauth.Client(consumer, access_token)

dbclient = MongoClient("mongodb://localhost:27017/")
db = dbclient.SentimentAnalysis


def __init__(self, id):
    self.last_id = id


def getTweet(query, count, result_type, max_id, search_by, search_value, is_next, id_desc):

    method = "GET"
    headers = "{'Content-type': 'application/json'}"

    if(max_id != None):
        url = "https://api.twitter.com/1.1/search/tweets.json" + \
            "?q="+query+"&count="+count+"&result_type="+result_type+ \
            "&max_id="+max_id
    else:
        url = "https://api.twitter.com/1.1/search/tweets.json" + \
            "?q="+query+"&count="+count+"&result_type="+result_type

    print(method)
    print(url)
    print(headers)
    # print(search_by)
    # print(search_value)

    try:
        response, data = client.request(url, method=method, headers=headers)

        # print(response)
        # print(str(data))

        tweets_data = json.loads(data)
        # print(tweets_data)

        # save to file
        # fh = open("json_result.txt", "w")
        # fh.write(json.dumps(tweets_data))
        # fh.close()

        saved_id = None
        temp = None
        i = 0
        max = len(tweets_data["statuses"])
        print("count data : " + str(max))

        # jika jumlah data dari respon > 0, maka lanjut
        if(max > 0):

            # pengulangan array
            for tweet in tweets_data["statuses"]:

                # jika data nomor 1, tidak akan dilayani
                if(i == 0):
                    i = i+1
                    temp = tweet["id_str"]

                # data selanjutnya yang akan diyani
                else:
                    
                    # jika data saat ini lebih kecil dari sebelumnya, maka dilayani
                    if(tweet["id_str"] < temp):

                        # set new temporary
                        temp = tweet["id_str"]
                        i = i+1

                        # set data-data tambahan untuk di insert
                        tweet["mongo_created_at"] = datetime.datetime.now()
                        tweet["search_by"] = search_by
                        tweet["search_value"] = search_value
                        tweet["scoring_progress"] = False
                        tweet["scoring_progress_date"] = ""
                        tweet["scoring_point"] = ""
                        tweet["scoring_sentiment"] = ""

                        # jika ada nilai retweeted, maka diabaikan
                        if "retweeted_status" in tweet:
                            # print("(%i) %i %s @%s %s" % (i, len(tweet["retweeted_status"]), tweet["id_str"], tweet["created_at"], tweet["text"][:10]))
                            pass
                            
                        # jika tidak ada nilai retweeted, maka dilayani penyimpanan data
                        else:
                            print("(%i) %i %s @%s %s" % (i, 0, tweet["id_str"], tweet["created_at"], tweet["text"][:10]))
                            db.tweets_daily.insert_one(tweet)
                            
                            topics = db.topics.find({"type": tweet['search_by'], "value": tweet['search_value']}).sort('_id', 1).limit(1) 
                            count_all = int(topics[0]['count_all']) + 1
                            db.topics.update({"type": tweet['search_by'], "value": tweet['search_value']},
                            {"$set" : {
                                "count_all": bson.int64.Int64(count_all), 
                            }})
                            
                            saved_id = tweet["id_str"]
                        

                        # jika data tweet saat ini lebih besar dari id desc, maka dilayani
                        if(int(str(tweet["id"])) >= int(str(id_desc))): 

                            #jika data loop habis 
                            if(i == max-1):
                                max_id = str(tweet["id"])
                                is_next = True
                                #update max_id di database
                                if(saved_id):
                                    db.topics.update({"type": search_by, "value": search_value}, {"$set" : {"max_id": bson.int64.Int64(saved_id)}})
                                #loop get tweet lagi
                                getTweet(query, count, result_type, max_id, search_by, search_value, is_next, id_desc)

                        #jika tweet saat ini lebih kecil atau sama dengan id desc, maka stop
                        else: 
                            #jika ada saved_id
                            if(saved_id):
                                #update max_id di database jadi 0, supaya bisa cari data yang baru
                                db.topics.update({"type": search_by, "value": search_value}, {"$set" : {"max_id": bson.int64.Int64("0")}})
                                #update id_desc, supaya acuan data baru
                                id_desc_new = db.tweets_daily.find({"search_by": search_by, "search_value": search_value}).sort('id', -1).limit(1)
                                db.topics.update({"type": search_by, "value": search_value}, {"$set" : {"id_desc": bson.int64.Int64(id_desc_new[0]['id']), "created_at_desc": id_desc_new[0]['created_at'], "mongo_created_at_desc": id_desc_new[0]['mongo_created_at']}})
                        
                        
    except Exception as e:
        print(e)


def getTopic():

    i = 0
    search_by = "keyword"
    search_value = "prabowo"

    print("================================")
    print("start topic")
    print("================================")
    print("topic index : " + str(i))
    print("search_by : " + search_by)
    print("search_value : " + search_value)
    print("================================")

    result_id = db.topics.find({"type": search_by, "value": search_value}).sort('_id', -1).limit(1)

    # print(result_id.count())
    # print(result_id[0]['_id_asc'])
    # print(result_id[0]['_id_desc'])
    # print(result_id[0]['id_asc'])
    # print(result_id[0]['id_desc'])
    # print(result_id[0]['max_id'])
 
    count = "100"
    result_type = "recent"
    max_id = None
    is_next = False 
    id_desc = result_id[0]['id_desc']

    if(search_by == "hashtag"):
        query = "%23"+search_value
    elif(search_by == "keyword"):
        query = search_value
    else:
        query = search_value

    if(result_id[0]['max_id'] == 0):
        max_id = None
    else:
        max_id = str(result_id[0]['max_id'])
 
    getTweet(query, count, result_type, max_id, search_by, search_value, is_next, id_desc)


if __name__ == '__main__':
    getTopic()
    # main()
 

import requests 
import json
import logging
   
def main():
     
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


    english = open("SentiWordNet_3.0.0_20130122_English.txt","r")
    english_text = english.readlines()
    
    
    i=0
    for eng_txt in english_text:
        i=i+1
        if i>=4140:
            eng_txt_arr = eng_txt.split("	")
            logger1.info(str(i))
            logger1.info("======= ") 
            logger1.info(eng_txt_arr[4])
            logger1.info(eng_txt_arr[5].replace("\n","")) 
            eng_txt_word = eng_txt_arr[4].split(" ")  
 
            URL = "https://translation.googleapis.com/language/translate/v2?key=" 
            PARAMS = {"format":"text", "model":"nmt", "source": "en", "target": "id", "q":[]}
            HEADERS = {"content-type":"application/json"}
            for word in eng_txt_word: 
                real_word = word.split("#") 
                PARAMS["q"].append(real_word[0])
         
            eng_txt_arr[5] = eng_txt_arr[5].replace('`',"'")
            eng_txt_arr[5] = eng_txt_arr[5].replace('`',"'")
            eng_txt_arr[5] = eng_txt_arr[5].replace('"',"'")
            eng_txt_arr[5] = eng_txt_arr[5].replace("\n","")
            PARAMS["q"].append(eng_txt_arr[5]) 
            logger1.info(PARAMS)

            try:
                translate = requests.post(url = URL, params = PARAMS, headers = HEADERS, timeout=5) 
                response_translate = translate.json()  
                logger1.info(response_translate)

                try:  
                    data = response_translate["data"]
                    translations = data["translations"] 

                    j = 0 
                    eng_txt_arr[4] = ""
                    eng_txt_arr[5] = ""
                    for kata in translations:
                        j = j+1 
                        if j < len(translations):
                            eng_txt_arr[4] = eng_txt_arr[4] + kata["translatedText"] + "#" + str(j)
                            if j < (len(translations)-1):
                                eng_txt_arr[4] = eng_txt_arr[4] + " "

                        if j == len(translations):
                            eng_txt_arr[5] = eng_txt_arr[5] + kata["translatedText"] + "\n"
                            eng_txt_arr[5] = eng_txt_arr[5].replace("\u200b"," ")

                except Exception as e:
                    logger1.error("Error read json result")
                    logger1.error(e) 
                
            except Exception as e:
                logger1.error("Error POST to Google Translate")
                logger1.error(e)  
            
             
            logger1.info(eng_txt_arr[4])
            logger1.info(eng_txt_arr[5])  


            indonesia = open("SentiWordNet_3.0.0_20130122_Indonesia.txt","a+")
            indonesia.write(eng_txt_arr[0] + "	" + eng_txt_arr[1] + "	" + eng_txt_arr[2] + "	" + eng_txt_arr[3] + "	" + eng_txt_arr[4] + "	" + eng_txt_arr[5])
            indonesia.close()

    english.close()


if __name__ == '__main__':  
    main()
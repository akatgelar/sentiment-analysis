import requests 
import json
import logging
import urllib 
from time import sleep
import gspread
from oauth2client.service_account import ServiceAccountCredentials

  
def GoogleTranslate(text): 
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)

    gc = gspread.authorize(credentials)
    wks = gc.open("service-translator-sentiment-analysis").sheet1
    wks.update_acell('A1', '=gTranslate("'+text+'", "en", "id")')
    cell_list = wks.acell('A1').value

    #print(cell_list)

    return cell_list
 

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
        if i>=4340:
            eng_txt_arr = eng_txt.split("	")
            logger1.info(str(i))
            logger1.info("======= ") 
            eng_txt_word = eng_txt_arr[4].split(" ")  
   
            # translate per kata
            j = 0 
            eng_txt_arr[4] = "" 

            for word in eng_txt_word: 
                real_word = word.split("#")  
                try:
                    sleep(5)
                    response_translate = GoogleTranslate(real_word[0])
                    # logger1.info(real_word[0])
                    # logger1.info(response_translate)
                    # logger1.info("-------------------------------") 
                    j = j+1 
                    if j <= len(eng_txt_word):
                        eng_txt_arr[4] = eng_txt_arr[4] + response_translate + "#" + str(j)
                        if j <= (len(eng_txt_word)-1):
                            eng_txt_arr[4] = eng_txt_arr[4] + " "
                except Exception as e:
                    logger1.error("Error POST to Google Translate")
                    logger1.error(e)  
                

            # translate deskripsi kalimat
            eng_txt_arr[5] = eng_txt_arr[5].replace('`',"'")
            eng_txt_arr[5] = eng_txt_arr[5].replace('`',"'")
            eng_txt_arr[5] = eng_txt_arr[5].replace('"',"'")
            eng_txt_arr[5] = eng_txt_arr[5].replace("\n","") 
            
            try:
                sleep(5) 
                response_translate = GoogleTranslate(eng_txt_arr[5])
                # logger1.info(eng_txt_arr[5])
                # logger1.info(response_translate)
                # logger1.info("-------------------------------")  
                eng_txt_arr[5] = ""
                eng_txt_arr[5] = eng_txt_arr[5] + response_translate + "\n"
                eng_txt_arr[5] = eng_txt_arr[5].replace("\u200b"," ")
            except Exception as e:
                logger1.error("Error POST to Google Translate")
                logger1.error(e)  
 
            logger1.info(eng_txt_arr[4])
            logger1.info(eng_txt_arr[5])  


            # indonesia = open("SentiWordNet_3.0.0_20130122_Indonesia.txt","a+")
            # indonesia.write(eng_txt_arr[0] + "	" + eng_txt_arr[1] + "	" + eng_txt_arr[2] + "	" + eng_txt_arr[3] + "	" + eng_txt_arr[4] + "	" + eng_txt_arr[5])
            # indonesia.close()

    english.close()


if __name__ == '__main__':  
    main()
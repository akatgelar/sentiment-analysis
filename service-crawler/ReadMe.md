# Sentiment Analysis - Service Crawler



## About

This is service for crawling data from twitter



## Installation

If you are using windows,

First include the python to venv

```
py -3 -m venv venv
```

And activate the venv

```
venv\Scripts\activate
pip install -r requirement.txt
```

If you are using linux,

First include the python to venv

```
virtualenv -p python3.5 venv --no-site-packages
```

And activate the venv

```
source venv/bin/activate
pip install -r requirement.txt
```




# Usage

Edit twitter credential 

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_KEY = ""
ACCESS_SECRET = ""



Edit hashtag value

search_value= ""



And then, run the script

```
python crawler_daily.py
```



You can see the progress on terminal

And activity log on **log/access.log**
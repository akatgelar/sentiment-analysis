# Sentiment Analysis - Service Scoring

## About

This is service for scoring sentiment

- First translate indonesian tweet using google translate

- Then get sentiment scoring using SentiWordNet

  

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

Edit google sheet client_secret.json

`{
  "type": "",
  "project_id": "",
  "private_key_id": "",
  "private_key": "",
  "client_email": "",
  "client_id": "",
  "auth_uri": "",
  "token_uri": "",
  "auth_provider_x509_cert_url": "",
  "client_x509_cert_url": ""
}`

And then, run the script

```
python scoring-english.py
```



You can see the progress on terminal

And activity log on **log/access.log**

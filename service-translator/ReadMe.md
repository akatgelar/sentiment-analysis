# Sentiment Analysis - Service Translator



## About

This is service for translating SentiWordNet English version to  Indonesia version

Using google translate API and google sheet API



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

Edit google translate key

` URL = "https://translation.googleapis.com/language/translate/v2?key=" `

And then, run the script

```
python translator.py
```



You can see the progress on terminal

See the result data on **SentiWordNet_3.0.0_20130122_Indonesia.txt** file

And activity log on **log/access.log**


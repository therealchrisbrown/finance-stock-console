# Simple Finance Console
Track your stocks & ideas and get a simple overview

# How to use

Install

```
pip install requirements.txt
```

Or

```
pipenv install
pipenv shell
```

## API KEYS

You also need several secrets from the official Twitter API. Just go to https://developer.twitter.com/en and create an account.

For Alphavantage: to get historical stock data you'll need an api key from alphavantage - it is free. Just go to https://www.alphavantage.co/ and create an account. You will get your free API Key immediately.

# Start the console

```
streamlit run finance_console.py
```

# IMPORTANT: auth .env-File

To use the console successfully, it is necessary to create an .env file.

## The File must contain the following

TWITTER_CONSUMER_KEY=

TWITTER_CONSUMER_SECRET=

TWITTER_ACCESS_TOKEN=

TWITTER_ACCESS_TOKEN_SECRET=

AV_APIKEY=

# Special thanks to parttimelarry for the great input and tutorial!

Check him out: https://github.com/hackingthemarkets @hackingthemarkets

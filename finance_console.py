import streamlit as st
import pandas as pd
import numpy as np
import requests
import tweepy
import matplotlib.pyplot as plt
from matplotlib import dates, style
import plotly.graph_objects as go
import datetime
import yfinance as yf
from decouple import config
import twitter_user


auth = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'), config('TWITTER_CONSUMER_SECRET'))
auth.set_access_token(config('TWITTER_ACCESS_TOKEN'), config('TWITTER_ACCESS_TOKEN_SECRET'))

api = tweepy.API(auth)


st.sidebar.title("Console")
st.sidebar.text("Investing")


option = st.sidebar.selectbox("Welches Dashboard?", ('Company Overview','Stocktwits', 'Strategies', 'Twitter', 'wallstreetbets'))
st.title(option)


if option == 'Company Overview':
    ticker = st.sidebar.text_input("Ticker", value='', max_chars=10)
    stock = yf.Ticker(ticker)
    info = stock.info

    left_column1, right_column1 = st.beta_columns(2)
    company_name = left_column1.subheader(info['longName'])
    sector_company = left_column1.markdown(info['sector'])
    industry_company = left_column1.markdown(info['industry'])
    company_logo = right_column1.image(info['logo_url'])
    company_country = left_column1.write(info['country'])
    company_website = left_column1.write(info['website'])

    st.markdown('#')

    with st.beta_expander("Was macht das Unternehmen?"):
        st.write(info['longBusinessSummary'])
    
    st.markdown('#')

    with st.beta_expander("Latest News"):
        st.write("Test")

    st.markdown('#')

    with st.beta_expander("Finanzüberblick"):
        st.write(info)
    
    st.markdown('#')

    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol="+ticker+"&outputsize=full&apikey="
    params_adjclose= {'function': 'TIME_SERIES_DAILY_ADJUSTED', 'symbol': ticker, 'outputsize': 'full', 'apikey': config('AV_APIKEY')}
    params_val = {'function': 'INCOME_STATEMENT', 'symbol': ticker, 'outputsize': 'full', 'apikey': config('AV_APIKEY')}
    
    left_column2, right_column2 = st.beta_columns(2)
    startdate = left_column2.date_input("Von:", datetime.date(2018,1,1))
    enddate = right_column2.date_input("Bis:")
    pressed = st.button("Go!")
    
    if pressed:

        r_adjclose = requests.get(url, params_adjclose)
        data_adjclose = r_adjclose.json()
        df_adjclose = pd.DataFrame.from_dict(data_adjclose['Time Series (Daily)'], orient="index")
        df_adjclose = df_adjclose.astype(float)
        df_adjclose = df_adjclose.loc[str(enddate):str(startdate)]
        df_adjclose_clean = df_adjclose['5. adjusted close']

        fig_adjclose = go.Figure(
             data = go.Scatter(x=df_adjclose_clean.index, y=df_adjclose_clean)
        )
        st.plotly_chart(fig_adjclose, use_container_width=True)

    # r_val = requests.get(url, params_val)
    # data_val = r_val.json()
    # df_val = pd.DataFrame.from_dict(data_val['quarterlyReports'])
    # df_val = df_val.reset_index()

    # fig_rev = go.Figure(
    #     data = go.Scatter(x=df_val['fiscalYearEnding'], y=df_val['totalRevenue'])
    # )
    # st.plotly_chart(fig_rev, use_container_width=True)

    # st.write(df_val)


if option == 'Stocktwits':
    ticker = st.sidebar.text_input("Ticker", value='', max_chars=10)

    
    r = requests.get(f'https://api.stocktwits.com/api/2/streams/symbol/{ticker}.json')
    
    data = r.json()
    
    for message in data['messages']:
        st.write(message['user']['username'])
        st.write(message['created_at'])
        st.write(message['body'])

if option == 'Strategies':
    st.subheader('Markowitz')

if option == 'Twitter':
    for username in twitter_user.TWITTER_USERNAMES:
        user = api.get_user(username)

        tweets = api.user_timeline(username)

        st.header(username)

        for tweet in tweets:
            if '$' in tweet.text:
                words = tweet.text.split(' ')
                for word in words:
                    if word.startswith('$') and word[1:].isalpha():
                        symbol = word[1:]
                        st.write(symbol)
                        st.write(tweet.text)
                        st.image(f"https://finviz.com/chart.ashx?t={symbol}")
    

if option == 'wallstreetbets':
    st.subheader("Sentiment Analyse - t.b.a.")

    left_column, right_column = st.beta_columns(2)
    pressed = left_column.button('Press me?')
    if pressed:
        right_column.write("Woohoo!")

    expander = st.beta_expander("FAQ")
    expander.write("Here you could put in some really, really long explanations...")

#tba

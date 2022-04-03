import streamlit as st
from multiapp import MultiApp
from apps import home, news_sentiment, arima,MACD,BollingerBand,monte_carlo# import your app modules here
from time import strftime
from tracemalloc import start
from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import copy
from datetime import date 
import datetime 

app = MultiApp()

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Stocks News Sentiment Analysis", news_sentiment.app)
app.add_app("ARIMA", arima.app)
app.add_app("MACD", MACD.app)
app.add_app("Bollinger Band", BollingerBand.app)
app.add_app("Monte Carlo", monte_carlo.app)
# The main app
app.run()

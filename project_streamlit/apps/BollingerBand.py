from time import strftime
from tracemalloc import start
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st
import copy

def app():
    st.image('./meta.jpg')
    close_data = st.session_state['close_data']
    columns=close_data.columns
    columns_list=columns.tolist()

    df = copy.deepcopy(close_data)


    def get_sma(prices, rate):
        return prices.rolling(rate).mean()

    def get_bollinger_bands(prices, rate=20):
        sma = get_sma(prices, rate)
        std = prices.rolling(rate).std()
        bollinger_up = sma + std * 2 # Calculate top band
        bollinger_down = sma - std * 2 # Calculate bottom band
        return bollinger_up, bollinger_down

    stock = st.selectbox(
     'Choose a stock to display its Bollinger Band',
      columns_list)

    bollinger_up, bollinger_down = get_bollinger_bands(df[stock])

    df["bollinger up"] = bollinger_up
    df["bollinger down"] = bollinger_down
    #st.write(df)

    fig=plt.figure(figsize=(16,8))
    plt.style.use('fivethirtyeight')
    plt.title(stock + ' Bollinger Bands')
    plt.xlabel('Days')
    plt.ylabel('Closing Prices')
    plt.plot(df[stock], label=stock+' Closing Prices')
    plt.plot(bollinger_up, label='Bollinger Up', c='g')
    plt.plot(bollinger_down, label='Bollinger Down', c='r')
    plt.legend()
    plt.show()
    st.pyplot(fig)
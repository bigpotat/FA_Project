from re import S
from time import strftime
from tracemalloc import start
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st
import copy
from matplotlib import *

def app():
    st.image('./meta.jpg')
    close_data = st.session_state['close_data']
    columns=close_data.columns
    columns_list=columns.tolist()

    df = copy.deepcopy(close_data)
    st.write(df)


    def get_sma(prices, rate):
        return prices.rolling(rate).mean()

    def get_bollinger_bands(prices, rate=20):
        sma = prices.rolling(rate).mean()
        std = prices.rolling(rate).std()
        bollinger_up = sma + std * 2 # Calculate top band
        bollinger_down = sma - std * 2 # Calculate bottom band
        return (bollinger_up, bollinger_down)

    stock = st.selectbox(
     'Choose a stock to display its Bollinger Band',
      columns_list)

    bollinger_up, bollinger_down = get_bollinger_bands(df[stock])
    df["bollinger_up"]=bollinger_up
    df["bollinger_down"]=bollinger_down
    df['Buy_Signal'] = np.where(df.bollinger_down > df[stock], True, False)
    df['Sell_Signal'] = np.where(df.bollinger_up < df[stock], True, False)
    
    buys = []
    sells = []
    open_position = False

    for i in range(len(df)):
        if df.bollinger_down[i] > df[stock][i]:
            if open_position == False:
                buys.append(i)
                open_position = True
        elif df.bollinger_up[i] < df[stock][i]:
            if open_position:
                sells.append(i)
                open_position = False
    
    fig=plt.figure(figsize=(12.2,6.4))
    x_axis=df.index
    plt.fill_between(x_axis,df['bollinger_up'],df['bollinger_down'],facecolor='blue', alpha=0.3,label="Bollinger")
    plt.scatter(df.iloc[buys].index, df.iloc[buys][stock], marker='^', color ='g',s=10*np.array(5)**2)
    plt.scatter(df.iloc[sells].index, df.iloc[sells][stock], marker='v', color ='r',s=10*np.array(5)**2)
    plt.plot(df[stock],label="Close Price",color="gold",alpha=0.7)
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("Bollinger Band")
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()
    st.pyplot(fig)

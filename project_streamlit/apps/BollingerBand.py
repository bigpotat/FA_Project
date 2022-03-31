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
    st.write(df)


    def get_sma(prices, rate):
        return prices.rolling(rate).mean()

    def get_bollinger_bands(prices, rate=20):
        sma = get_sma(prices, rate)
        std = prices.rolling(rate).std()
        bollinger_up = sma + std * 2 # Calculate top band
        bollinger_down = sma - std * 2 # Calculate bottom band
        return bollinger_up, bollinger_down
    
    def get_signal(data):
        buys = []
        sells = []

        for i in range(len(data[stock])):
            if data["bollinger down"][i] > data[stock][i]:
                buys.append(data[stock][i])
                sells.append(np.nan)

            elif data["bollinger up"][i] < data[stock][i]:
                sells.append(data[stock][i])
                buys.append(np.nan)
            else:
                sells.append(np.nan)
                buys.append(np.nan)
        return(buys,sells)

    stock = st.selectbox(
     'Choose a stock to display its Bollinger Band',
      columns_list)

    bollinger_up, bollinger_down = get_bollinger_bands(df[stock])

    df["bollinger up"] = bollinger_up
    df["bollinger down"] = bollinger_down
    df["Buy"]=get_signal(df)[0]
    df["Sell"]=get_signal(df)[1]
    #st.write(df)

    fig=plt.figure(figsize=(12.2,6.4))
    x_axis=df.index
    plt.fill_between(x_axis,df['bollinger up'],df['bollinger down'],facecolor='blue', alpha=0.3,label="Bollinger")
    plt.scatter(df.index,df["Buy"],color="green",label="Buy",marker="^",s=100)
    plt.scatter(df.index,df["Sell"],color="red",label="Sell",marker="v",s=100)
    plt.plot(df[stock],label="Close Price",color="gold",alpha=0.5)
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("Bollinger Band")
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()
    st.pyplot(fig)

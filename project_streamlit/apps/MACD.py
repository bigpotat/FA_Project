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
    #st.write(columns_list)
    #st.write(type(columns_list))


    MACD = copy.deepcopy(close_data)

    def calculate_MACD(stock):
        df=MACD[stock].to_frame()
        df["long_term_EMA"]=df[stock].ewm(span=26,adjust=False).mean() #long term EMA 
        df["short_term_EMA"]=df[stock].ewm(span=12,adjust=False).mean() #short term EMA 
        df["MACD"]=df["short_term_EMA"]-df["long_term_EMA"]           #MACD line
        df["Signal_line"]=df["MACD"].ewm(span=9,adjust=False).mean() # Signal line 
            
        return(df)

    def buy_sell(signal):
        Buy=[]
        Sell=[]
        flag= -1 
        
        
        for i in range(0,len(signal)):
            if signal["MACD"][i] > signal["Signal_line"][i]:
                Sell.append(np.nan)
                if flag != 1 :
                    Buy.append(signal[stock][i])
                    flag=1 
                else:
                    Buy.append(np.nan)
            
            elif signal["MACD"][i] < signal["Signal_line"][i]:
                Buy.append(np.nan)
                if flag != 0 :
                    Sell.append(signal[stock][i])
                    flag= 0
                else:
                    Sell.append(np.nan)
            else:
                Buy.append(np.nan)
                Sell.append(np.nan)
        return (Buy,Sell)

    stock = st.selectbox(
     'Choose a stock to display its MACD',
      columns_list)

    df=calculate_MACD(stock)

    st.header("Here is MACD indicator")
    fig=plt.figure(figsize=(16,8))
    plt.style.use('fivethirtyeight')
    plt.plot(df.index,df["MACD"],label=stock+" MACD",color="red")
    plt.plot(df.index,df["Signal_line"],label=stock+" Signal_line",color="blue")
    plt.legend(loc="upper left")
    plt.show()
    st.pyplot(fig)

    a=buy_sell(df)
    df['Buy_Signal_Price']=a[0]
    df["Sell_Signal_Price"]=a[1]

    fig=plt.figure(figsize=(16,8))
    plt.title(stock + ' MACD')
    plt.scatter(df.index,df["Buy_Signal_Price"],color="green",label="Buy",marker="^",alpha=1)
    plt.scatter(df.index,df["Sell_Signal_Price"],color="red",label="Sell",marker="v",alpha=1)
    plt.plot(df[stock],label="Close Price",alpha=0.35)
    plt.title(stock+":Close Price Buy & Sell Signals")
    plt.xlabel("Date")
    plt.ylabel("Close Price in USD")
    plt.legend(loc="upper left")
    plt.show()
    st.pyplot(fig)

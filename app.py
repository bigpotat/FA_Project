from time import strftime
from tracemalloc import start
from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st
import copy
from datetime import date 
import datetime 

st.image('./meta.jpg')
st.title("Financial Analytics Team Project Team 1 MetaVerse")

tickers = st.multiselect(
     'Choose one or multiple stock to display the return series and other technical indicators',
     ['FSLY','IMMR', 'FB', 'U','NVDA','AAPL','MSFT',"METV"],
     ["METV"])


start_date=st.date_input(label="Starting Date",value=datetime.date(2021,7,1))
end_date=st.date_input("End Date",value=datetime.date(2022,3,1))

today=date.today()

if start_date >= end_date:
    st.error('Error: End date must fall after start date.')
elif end_date>today:
    st.error("Error: End date can not after today ")

start_date=start_date.strftime('%Y-%m-%d')
end_date=end_date.strftime('%Y-%m-%d')

panel_data = data.DataReader(tickers,'yahoo', start_date, end_date)

data = panel_data[['Close', 'Adj Close']]
close_data = panel_data['Close']
adj_close_data = panel_data['Adj Close']

return_series_adj = (adj_close_data.pct_change()+ 1).cumprod() - 1
st.write(return_series_adj)


fig=plt.figure(figsize=(16,8))
plt.style.use('fivethirtyeight')
for ticker in tickers:
    plt.plot(return_series_adj[ticker],label=ticker)
plt.legend()
plt.title("Return Series")
plt.show()
st.pyplot(fig)
#st.plotly_chart(fig)

TechIndicator = copy.deepcopy(data)
MACD=TechIndicator["Close"]

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
     'Choose a stock',
     tickers)

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
plt.scatter(df.index,df["Buy_Signal_Price"],color="green",label="Buy",marker="^",alpha=1)
plt.scatter(df.index,df["Sell_Signal_Price"],color="red",label="Sell",marker="v",alpha=1)
plt.plot(df[stock],label="Close Price",alpha=0.35)
plt.title(stock+":Close Price Buy & Sell Signals")
plt.xlabel("Date")
plt.ylabel("Close Price in USD")
plt.legend(loc="upper left")
plt.show()
st.pyplot(fig)
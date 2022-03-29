import streamlit as st
from time import strftime
from tracemalloc import start
from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import copy
from datetime import date 
import datetime 
def app():
    ## upload title and image 
    #st.image('/jiaxin_streamlit/meta.jpg')
    st.title("Financial Analytics Team Project Team 1 MetaVerse")   
    
    ## let user choose stock and date
    tickers = st.multiselect(
        'Choose one or multiple stock to display the return series and other technical indicators',
        ['FSLY','IMMR', 'FB', 'U','NVDA','AAPL','MSFT',"METV"],
        ["METV"])
    start_date=st.date_input(label="Starting Date",value=datetime.date(2021,7,1))
    end_date=st.date_input("End Date",value=datetime.date(2022,3,1))
    st.write("This is the return series for the selected stock(s) in table form")
    today=date.today()

    if start_date >= end_date:
        st.error('Error: End date must fall after start date.')
    elif end_date>today:
        st.error("Error: End date can not after today ")

    start_date=start_date.strftime('%Y-%m-%d')
    end_date=end_date.strftime('%Y-%m-%d')

    ## Get data for stock
    panel_data = data.DataReader(tickers,'yahoo', start_date, end_date)
    # data = panel_data[['Close', 'Adj Close']]
    close_data = panel_data['Close']
    adj_close_data = panel_data['Adj Close']
   
    st.session_state['close_data'] = close_data
    st.session_state['adj_close_data'] = adj_close_data
    # st.write(st.session_state)
    # generate return series diagram
    
    return_series_adj = (adj_close_data.pct_change()+ 1).cumprod() - 1
    st.write(return_series_adj)
    fig=plt.figure(figsize=(16,8))
    plt.style.use('fivethirtyeight')
    st.write("This is the return series for the selected stock(s) in line chart form")
    for ticker in tickers:
        plt.plot(return_series_adj[ticker],label=ticker)
    plt.legend()
    plt.title("Return Series")
    plt.show()
    st.pyplot(fig)
    #st.plotly_chart(fig)
import streamlit as st
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import os
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
from pmdarima.arima import auto_arima
from sklearn.metrics import mean_squared_error, mean_absolute_error
import math


def app():
    st.title('ARIMA')

    close_data = st.session_state['close_data']
    st.write("An autoregressive integrated moving average, or ARIMA, is a statistical analysis model ")
    st.write("that uses time series data to either better understand the data set or to predict future trends")

    ticker = st.selectbox(
        'Choose one or multiple stock to display the return series and other technical indicators',
        ['FSLY','IMMR', 'FB', 'U','NVDA','AAPL','MSFT',"METV"],0)

    
    ticker_close=close_data[ticker].to_frame()

    #Test for stationarity
    def test_stationarity(timeseries):
        #Determing rolling statistics
        rolmean = timeseries.rolling(12).mean()
        rolstd = timeseries.rolling(12).std()
        #Plot rolling statistics:
        fig=plt.figure(figsize=(16,8))
        plt.plot(timeseries, color='blue',label='Original')
        plt.plot(rolmean, color='red', label='Rolling Mean')
        plt.plot(rolstd, color='black', label = 'Rolling Std')
        plt.legend(loc='best')
        plt.title('Rolling Mean and Standard Deviation')
        plt.show(block=False)
        st.pyplot(fig)
        st.write("Results of dickey fuller test")
        adft = adfuller(timeseries,autolag='AIC')
        # output for dft will give us without defining what the values are.
        #hence we manually write what values does it explains using a for loop
        output = pd.Series(adft[0:4],index=['Test Statistics','p-value','No. of lags used','Number of observations used'])
        for key,values in adft[4].items():
            output['critical value (%s)'%key] =  values
        st.write(output)
    test_stationarity(ticker_close)

    #To separate the trend and the seasonality from a time series, 
    st.write("Decompose the series")
    result = seasonal_decompose(ticker_close, model='multiplicative', period = 30)
    fig = plt.figure()  
    fig = result.plot()  
    fig.set_size_inches(16, 9)
    st.pyplot(fig)

    #if not stationary then eliminate trend
    st.write('Eliminate trend')
    from pylab import rcParams
    rcParams['figure.figsize'] = 10, 6
    df_log = np.log(ticker_close)
    moving_avg = df_log.rolling(12).mean()
    std_dev = df_log.rolling(12).std()
    fig = plt.figure(figsize=(16,9))
    plt.legend(loc='best')
    plt.title('Moving Average')
    plt.plot(std_dev, color ="black", label = "Standard Deviation")
    plt.plot(moving_avg, color="red", label = "Mean")
    plt.legend()
    plt.show()
    st.pyplot(fig)

    st.write("Split data into train and training set")
    train_data, test_data = df_log[3:int(len(df_log)*0.9)], df_log[int(len(df_log)*0.9):]
    fig=plt.figure(figsize=(10,6))
    plt.grid(True)
    plt.xlabel('Dates')
    plt.ylabel('Closing Prices')
    plt.plot(df_log, 'green', label='Train data')
    plt.plot(test_data, 'blue', label='Test data')
    plt.legend()
    st.pyplot(fig)

    model_autoARIMA = auto_arima(train_data, start_p=0, start_q=0,
                      test='adf',       # use adftest to find optimal 'd'
                      max_p=3, max_q=3, # maximum p and q
                      m=1,              # frequency of series
                      d=None,           # let model determine 'd'
                      seasonal=False,   # No Seasonality
                      start_P=0, 
                      D=0, 
                      trace=True,
                      error_action='ignore',  
                      suppress_warnings=True, 
                      stepwise=True)
    st.write(model_autoARIMA.summary())
    fig=plt.figure()
    fig = model_autoARIMA.plot_diagnostics()
    fig.set_size_inches(16, 9)
    plt.show()
    st.pyplot(fig)

    #Modeling
    st.write("Build Model")
    model = ARIMA(train_data, order=(1,1,2))  
    fitted = model.fit()  
    st.write(fitted.summary())

    st.write('Forecast')
    #fc, se, conf = fitted.forecast(13, alpha=0.05)  # 95% conf

    # report performance
    if (ticker == "FSLY"):
        st.image("./asset/fsly_arima_forecast.png")
        st.image("./asset/fsly_arima_perf.png")
    elif (ticker == "IMMR"):
        st.image("./asset/immr_arima_forecast.png")
        st.image("./asset/immr_arima_perf.png")
    elif (ticker == "FB"):
        st.image("./asset/fb_arima_forecast.png")
        st.image("./asset/fb_arima_perf.png")
    elif (ticker == "U"):
        st.image("./asset/u_arima_forecast.png")
        st.image("./asset/u_arima_perf.png")
    elif (ticker == "NVDA"):
        st.image("./asset/nvda_arima_forecast.png")
        st.image("./asset/nvda_arima_perf.png")
    elif (ticker == "AAPL"):
        st.image("./asset/aapl_arima_forecast.png")
        st.image("./asset/aapl_arima_perf.png")
    elif (ticker == "MSFT"):
        st.image("./asset/msft_arima_forecast.png")
        st.image("./asset/msft_arima_perf.png")
    elif (ticker == "METV"):
        st.image("./asset/metv_arima_forecast.png")
        st.image("./asset/metv_arima_perf.png")


    

    

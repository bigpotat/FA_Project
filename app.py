from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st
import altair as alt

st.header("Financial Analytics Team Project Team 1 MetaVerse")

tickers = ['FSLY','IMMR', 'FB', 'U','NVDA','AAPL', 'MSFT',"METV"]

start_date = '2021-07-01'
end_date = '2022-03-01'

panel_data = data.DataReader(tickers,'yahoo', start_date, end_date)
panel_data = panel_data.loc['2021-01-01' : '2021-12-31']

data = panel_data[['Close', 'Adj Close']]
close_data = panel_data['Close']
adj_close_data = panel_data['Adj Close']

return_series_adj = (adj_close_data.pct_change()+ 1).cumprod() - 1
st.write(return_series_adj)

fig=plt.figure(figsize=(16,8))
plt.style.use('fivethirtyeight')
plt.plot(return_series_adj.FSLY,label="FSLY")
plt.plot(return_series_adj.IMMR,label="IMMR")
plt.plot(return_series_adj.FB,label="FB")
plt.plot(return_series_adj.U,label="U")
plt.plot(return_series_adj.NVDA,label="NVDA")
plt.plot(return_series_adj.AAPL,label="AAPL")
plt.plot(return_series_adj.MSFT,label="MSFT")
plt.plot(return_series_adj.METV,label="METV")
plt.legend()
plt.title("Return Series")
plt.show()
st.pyplot(fig)
#st.plotly_chart(fig)


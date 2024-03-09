import streamlit as st 
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
from alpha_vantage.fundamentaldata import FundamentalData
from stocknews import StockNews
import pandas_ta as ta


st.title('Trading View By Epitome Consultancy')

ticker = st.sidebar.text_input('Ticker')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

data = yf.download(ticker, start = start_date, end = end_date)
fig = px.line(data , x = data.index , y = data['Adj Close'] , title = ticker)
st.plotly_chart(fig)

st.title('Technical Analysis Dashboard')
df = pd.DataFrame()
ind_list = df.ta.indicators(as_list = True)
#st.write(ind_list)
technical_indicator = st.selectbox('Tech Indicator', options = ind_list)
method = technical_indicator
indicator = pd.DataFrame(getattr(ta,method)(low = data['Low'], close = data['Close'], high = data['High'] , open = data['Open'], volume = data['Volume']))
indicator['Close'] = data['Close']

figW_ind_new = px.line(indicator)
st.plotly_chart(figW_ind_new)

st.write(indicator)

pricing_data , fundamental_data ,news = st.tabs(["Pricing Data","Fundamental Data","Top 10 News"])

with pricing_data:
    st.header('Price Movements')
    data2 = data 
    data2['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1) -1
    data2.dropna(inplace = True)
    st.write(data2)
    annual_return = data2['% Change'].mean()*250*100
    st.write("Annual Return is ", annual_return , '%')

    stdev = np.std(data2['% Change'])*np.sqrt(252)
    st.write('Standard Deviation is' , stdev*100 , '%')

    st.write('Risk Adj. Return is ', annual_return/(stdev*100))

# with fundamental_data:
#     key = 'OW1639L63B5UCYYL'
#     fd = FundamentalData(key , output_format = 'pandas')

#     st.subheader('Balance Sheet')
#     balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
#     bs = balance_sheet.T[2:]
#     bs.column  = list(balance_sheet.T.iloc[0])
#     st.write(bs)
    
#     st.subheader('Income Statement')
#     income_statement = fd.get_income_statement_annual(ticker)[0]
#     is1 = income_statement.T[2:]
#     is1.columns = list(income_statement.T.iloc[0])
#     st.write(is1)

#     st.subheader('Cash Flow Statement')
#     cash_flow = fd.get_cash_flow_annual(ticker)[0]
#     cf = cash_flow.T[2:]
#     cf.columns = list(cash_flow.T.iloc[0])
#     st.write(cf)

# with news:
#     st.header(f'News of {ticker}')
#     sn = StockNews(ticker , save_news = False)
#     df_news = sn.read_rss()
#     for i in range(10):
#         st.subheader(f'News {i+1}')
#         st.write(df_news['published'][i])
#         st.write(df_news['title'][i])
#         st.write(df_news['summary'][i])
#         title_sentiment = df_news['sentiment_title'][i]
#         st.write(f'Title Sentiment {title_sentiment}')
#         st.write(f'Title Sentiment {title_sentiment}')
#         news_sentiment = df_news['sentiment_summary'][i]
#         st.write(f'News Sentiments {news_sentiment}')





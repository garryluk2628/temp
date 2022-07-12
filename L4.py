import yfinance as yf
import streamlit as st
import pandas as pd
import datetime
tickerSymbol = 'AAPL'
tickerData = yf.Ticker(tickerSymbol)
tickerDf = tData.history(start=sd, end=ed)
st.write("""
# Simple Stock Price App
Shown the stock closing price, volume and simple return of the selected Stock!
""")
sd = st.date_input(
     "Start date",
     datetime.date(2019, 1, 1))

ed = st.date_input(
     "Start date",
     datetime.date(2022, 7, 1))


tickerSymbol = st.selectbox('Select the Stock that you like to plot graph', ('AAPL','TSLA','GOOG','MSFT','1211.HK','0011.HK')

#tickerSymbol = 'GOOGL'
#get data on this ticker
#tickerData = yf.Ticker(tickerSymbol)
#get the historical prices for this ticker			    
#define the ticker symbol
#tickerSymbol = option 
#get data on this ticker
#tickerData = yf.Ticker(tickerSymbol)
#get the historical prices for this ticker
#tickerDf = tData.history(start=sd, end=ed)
# Open	High	Low	Close	Volume	Dividends	Stock Splits
tickerDf['simple_rtn'] = tickerDf.Close.pct_change()

stock_close = ("Stock Close Price")
stock_volume = ("Stock Daily Volume")
stock_return = ("Stock Simple Return")

if option == 'AAPL':
	stock_name = 'APPLE Company'
elif option == 'TSLA':
	stock_name = 'Tesla Inc'
elif option == 'GOOG':
	stock_name = 'Google'
elif option == 'MSFT':
	stock_name = 'Microsoft'
elif option == '1211.HK':
	stock_name = 'BYD Company Limited'
elif option == '0011.HK':
	stock_name = 'Hang Seng Bank Limited'
else:
	stock_name = "  "
					


Stock_close_name = tickerSymbol + " " + stock_name + " " + stock_close
Stock_volume_name = tickerSymbol + " "  + stock_name + " " + stock_volume
Stock_return_name = tickerSymbol + " " + stock_name + " " + stock_return

st.title(Stock_close_name)
st.line_chart(tickerDf.Close)
st.title(Stock_volume_name)
st.line_chart(tickerDf.Volume)
st.title(Stock_return_name)
st.line_chart(tickerDf.simple_rtn)

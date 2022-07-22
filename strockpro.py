import pandas as pd
import numpy as np
import datetime
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices, greedy_portfolio
plt.style.use('fivethirtyeight')

options = st.multiselect(
     'What are your favorite Stocks',
     ['FB', 'AAPL', 'AMZN', 'NFLX','GOOG','TSLA','0011.HK','1211.HK'],
     ['AAPL','TSLA'])

st.write('You selected:', options)

length = len(options)
#for i in range(length):
#    weight[i] = st.number_input('Weigh of ',options[i],' is ')
#    st.write('The weight of ',option[i],' is ', weight[i])
weight = ((100 / length)/100)
wei = []
for i in range(length):
    wei.append(weight)
wei = np.array(wei)
st.write('the default weight for each stock:', weight)

sd = st.date_input(
     "Start date",
     datetime.date(2016, 1, 1))

ed = st.date_input(
     "Start date",
     datetime.date(2022, 7, 15))

df = pd.DataFrame()
df = yf.download(options,start=sd,end=ed)['Adj Close']


my_stock = df

if '1211.HK' in df.columns:
	df['1211.HK'] = df['1211.HK'].div(7.85).round(2)
	
if '0011.HK' in df.columns:
	df['0011.HK'] = df['0011.HK'].div(7.85).round(2)


st.subheader("Stock Price table")
df

st.subheader('Portfolio Adj close Price History')

plt.figure(figsize=(20, 8))
st.line_chart(my_stock)

#plt.title(title)
returns = df.pct_change()
cov_matrix_annual = returns.cov() * 252
st.write(cov_matrix_annual)
weit = np.transpose(wei)

st.write(weit)
port_variance = np.dot(weit,np.dot(cov_matrix_annual, wei))

port_volatility = np.sqrt(port_variance)

portfoilSimpAnnualRe = np.sum(returns.mean() * wei) * 252

percent_var = str(np.round(port_variance, 2)* 100) + '%'
percent_vols = str(np.round(port_volatility, 2)* 100) + '%'
percent_ret = str(np.round(portfoilSimpAnnualRe, 2)* 100) + '%'

st.write('Expected annual return: ' + percent_ret)
st.write('Annual volatility / risk: ' + percent_vols)
st.write('Annual variance: ' + percent_var)



mu = expected_returns.mean_historical_return(my_stock)

S = risk_models.sample_cov(my_stock)

ef = EfficientFrontier(mu,S)
weights = ef.max_sharpe()
cleaned_weights = ef.clean_weights()

st.write(cleaned_weights)

result = ef.portfolio_performance(verbose = True)
ear = np.round(result[0]*100,2)
AV = np.round(result[1]*100,2)
SR = result[2]
st.write('Expected annual return: ',ear,' %')
st.write('Annual volatility: ',AV,' %')
st.write('Sharpe Ratio: ',SR,' %')


invamount = st.number_input('What will be the total portfolio investment amount')
st.write('The Investment amount is ', invamount)

if invamount > 1:
	latest_prices = get_latest_prices(df)
	weights = cleaned_weights
	da = greedy_portfolio(weights, latest_prices, total_portfolio_value = invamount)
	#da = DiscreteAllocation(weights, latest_prices, total_portfolio_value = invamount)
	allocation,leftover = da.lp_portfolio()
	st.write('Discrete allocation: ',allocation)
	st.write('Funds remaining: $',round(leftover,2))

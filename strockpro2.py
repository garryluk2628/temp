import pandas as pd
import streamlit as st
import numpy as np
import datetime
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import copy
import plotly.express as px
plt.style.use('fivethirtyeight')
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import plotting

options = st.multiselect(
     'What are your favorite colors',
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

corr_df = cov_matrix_annual.round(2) # round to 2 decimal places
fig_corr = px.imshow(corr_df, text_auto=True, title = 'Correlation between Stocks')
fig_corr.show()


mu = expected_returns.mean_historical_return(df)
S = risk_models.sample_cov(df)
st.write(mu)

def plot_efficient_frontier_and_max_sharpe(mu, S):  
    # Optimize portfolio for maximal Sharpe ratio 
    ef = EfficientFrontier(mu, S)
    fig, ax = plt.subplots(figsize=(8,6))
    ef_max_sharpe = copy.deepcopy(ef)
    plotting.plot_efficient_frontier(ef, ax=ax, show_assets=False)
    # Find the max sharpe portfolio
    ef_max_sharpe.max_sharpe(risk_free_rate=0.02)
    ret_tangent, std_tangent, _ =   ef_max_sharpe.portfolio_performance()
    ax.scatter(std_tangent, ret_tangent, marker="*", s=100, c="r",     label="Max Sharpe")
# Generate random portfolios
    n_samples = 1000
    w = np.random.dirichlet(np.ones(ef.n_assets), n_samples)
    rets = w.dot(ef.expected_returns)
    stds = np.sqrt(np.diag(w @ ef.cov_matrix @ w.T))
    sharpes = rets / stds
    ax.scatter(stds, rets, marker=".", c=sharpes, cmap="viridis_r")
# Output
    ax.set_title("Efficient Frontier with Random Portfolios")
    ax.legend()
    plt.tight_layout()
    plt.show() 

plot_efficient_frontier_and_max_sharpe(mu, S) 

ef = EfficientFrontier(mu, S)
ef.max_sharpe(risk_free_rate=0.02)
weights = ef.clean_weights()
st.write(weights)

weights_df = pd.DataFrame.from_dict(weights, orient = 'index')
weights_df.columns = ['weights']
weights_df

expected_annual_return, annual_volatility, sharpe_ratio = ef.portfolio_performance()
st.write('Expected annual return: {}%'.format((expected_annual_return*100).round(2)))
st.write('Annual volatility: {}%'.format((annual_volatility*100).round(2)))
st.write('Sharpe ratio: {}'.format(sharpe_ratio.round(2)))



import yfinance as yf
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from datetime import datetime, timedelta, date

import finquant
from finquant.portfolio import build_portfolio
from finquant.efficient_frontier import EfficientFrontier
from finquant.moving_average import compute_ma, ema

st.set_page_config(
page_title="Portfolio Optimization Tools",
page_icon="📈",
layout="wide")

st.title("Portfolio Optimization Tools")
st.caption("Here is the tools for you, the investor, to build and optimize your own equity portfolio with Hang Seng Index (HSI).")
st.caption("Latest stock data are retrieved from Yahoo! Finance.")

HSI = ['0001.HK','0002.HK','0003.HK','0005.HK','0006.HK','0011.HK','0012.HK','0016.HK','0017.HK','0027.HK',
        '0066.HK','0101.HK','0175.HK','0241.HK','0267.HK','0288.HK','0291.HK','0316.HK','0386.HK','0388.HK',
        '0669.HK','0688.HK','0700.HK','0762.HK','0823.HK','0857.HK','0868.HK','0881.HK','0883.HK','0939.HK',
        '0941.HK','0960.HK','0968.HK','0981.HK','0992.HK','1038.HK','1044.HK','1093.HK','1109.HK','1113.HK',
        '1177.HK','1211.HK','1299.HK','1378.HK','1398.HK','1810.HK','1876.HK','1928.HK','1997.HK','2007.HK',
        '2020.HK','2269.HK','2313.HK','2318.HK','2319.HK','2331.HK','2382.HK','2388.HK','2628.HK','2688.HK',
        '3690.HK','3968.HK','3988.HK','6098.HK','6862.HK','9618.HK','9633.HK','9988.HK','9999.HK']

nameList = {
    '0001.HK': 'CKH HOLDINGS', '0002.HK': 'CLP HOLDINGS','0003.HK': 'HK & CHINA GAS', '0005.HK': 'HSBC HOLDINGS', 
    '0006.HK': 'POWER ASSETS', '0011.HK': 'HANG SENG BANK','0012.HK': 'HENDERSON LAND', '0016.HK': 'SHK PPT', 
    '0017.HK': 'NEW WORLD DEV', '0027.HK': 'GALAXY ENT','0066.HK': 'MTR CORPORATION', '0101.HK': 'HANG LUNG PPT', 
    '0175.HK': 'GEELY AUTO', '0241.HK': 'ALI HEALTH','0267.HK': 'CITIC', '0288.HK': 'WH GROUP', 
    '0291.HK': 'CHINA RES BEER', '0316.HK': 'OOIL','0386.HK': 'SINOPEC CORP', '0388.HK': 'HKEX', 
    '0669.HK': 'TECHTRONIC IND', '0688.HK': 'CHINA OVERSEAS','0700.HK': 'TENCENT', '0762.HK': 'CHINA UNICOM', 
    '0823.HK': 'LINK REIT', '0857.HK': 'PETROCHINA','0868.HK': 'XINYI GLASS', '0881.HK': 'ZHONGSHENG HLDG', 
    '0883.HK': 'CNOOC', '0939.HK': 'CCB','0941.HK': 'CHINA MOBILE', '0960.HK': 'LONGFOR GROUP', 
    '0968.HK': 'XINYI SOLAR', '0981.HK': 'SMIC','0992.HK': 'LENOVO GROUP', '1038.HK': 'CKI HOLDINGS', 
    '1044.HK': 'HENGAN INT L', '1093.HK': 'CSPC PHARMA','1109.HK': 'CHINA RES LAND', '1113.HK': 'CK ASSET', 
    '1177.HK': 'SINO BIOPHARM', '1211.HK': 'BYD COMPANY','1299.HK': 'AIA', '1378.HK': 'CHINAHONGQIAO', 
    '1398.HK': 'ICBC', '1810.HK': 'XIAOMI-W','1876.HK': 'BUD APAC', '1928.HK': 'SANDS CHINA LTD', 
    '1997.HK': 'WHARF REIC', '2007.HK': 'COUNTRY GARDEN','2020.HK': 'ANTA SPORTS', '2269.HK': 'WUXI BIO', 
    '2313.HK': 'SHENZHOU INTL', '2318.HK': 'PING AN','2319.HK': 'MENGNIU DAIRY', '2331.HK': 'LI NING', 
    '2382.HK': 'SUNNY OPTICAL', '2388.HK': 'BOC HONG KONG','2628.HK': 'CHINA LIFE', '2688.HK': 'ENN ENERGY', 
    '3690.HK': 'MEITUAN-W', '3968.HK': 'CM BANK','3988.HK': 'BANK OF CHINA', '6098.HK': 'CG SERVICES', 
    '6862.HK': 'HAIDILAO', '9618.HK': 'JD-SW','9633.HK': 'NONGFU SPRING', '9988.HK': 'BABA-SW', 
    '9999.HK': 'NTES-S'}
name_list = pd.DataFrame([nameList], index=['Company Name']).T
co_name = name_list['Company Name']

indList = {
    '0001.HK': 'Conglomerates','0002.HK' : 'Utilities','0003.HK': 'Utilities','0005.HK': 'Financials', 
    '0006.HK': 'Utilities', '0011.HK' : 'Financials','0012.HK': 'Properties & Construction', '0016.HK':'Properties & Construction',
    '0017.HK': 'Properties & Construction', '0027.HK': 'Consumer Discretionary','0066.HK': 'Consumer Discretionary', '0101.HK': 'Properties & Construction',
    '0175.HK': 'Consumer Discretionary', '0241.HK': 'Healthcare','0267.HK':'Conglomerates','0288.HK': 'Consumer Staples',
    '0291.HK':'Consumer Staples', '0316.HK': 'Industrials','0386.HK':'Energy', '0388.HK': 'Financials', 
    '0669.HK': 'Consumer Discretionary','0688.HK': 'Properties & Construction','0700.HK': 'Information Technology', '0762.HK': 'Telecommunications',
    '0823.HK': 'Properties & Construction', '0857.HK' : 'Energy','0868.HK': 'Industrials','0881.HK': 'Consumer Discretionary', 
    '0883.HK': 'Energy', '0939.HK': 'Financials','0941.HK': 'Telecommunications', '0960.HK' : 'Properties & Construction', 
    '0968.HK': 'Industrials', '0981.HK': 'Information Technology','0992.HK': 'Information Technology', '1038.HK' : 'Utilities',
    '1044.HK': 'Consumer Staples', '1093.HK': 'Healthcare','1109.HK': 'Properties & Construction', '1113.HK': 'Conglomerates',
    '1177.HK': 'Healthcare', '1211.HK': 'Consumer Discretionary','1299.HK': 'Financials', '1378.HK': 'Materials',
    '1398.HK': 'Financials', '1810.HK': 'Information Technology','1876.HK': 'Consumer Staples', '1928.HK': 'Consumer Discretionary',
    '1997.HK': 'Properties & Construction', '2007.HK': 'Properties & Construction','2020.HK': 'Consumer Discretionary', '2269.HK': 'Healthcare',
    '2313.HK': 'Consumer Discretionary', '2318.HK': 'Financials','2319.HK': 'Consumer Staples', '2331.HK': 'Consumer Discretionary',
    '2382.HK': 'Industrials', '2388.HK': 'Financials','2628.HK': 'Financials', '2688.HK': 'Utilities',
    '3690.HK': 'Information Technology', '3968.HK': 'Financials','3988.HK': 'Financials', '6098.HK': 'Properties & Construction',
    '6862.HK': 'Consumer Discretionary', '9618.HK': 'Information Technology','9633.HK': 'Consumer Staples', '9988.HK': 'Information Technology',
    '9999.HK': 'Information Technology'}
ind_list = pd.DataFrame([indList], index=['Industry']).T

# input stock symbol and data period
selectedStock = sorted(st.multiselect('Input the stock symbol: ',HSI))
years_list = ['1 years','2 years', '3 years', '4 years', '5 years']
selectedYear = st.selectbox('Years of historical stock price you would like to retrieved: ', years_list, index=1)
selectedYear = years_list.index(selectedYear) + 1

# contrist stock quantity within 2-20
if len(selectedStock) == 0:
    st.stop()
elif 0 < len(selectedStock) < 2:
    st.warning('Please select more than one stock for your portfolio. ')
    st.stop()
elif 20 < len(selectedStock):
    st.warning('Maximum underlying stocks quantity is 20. ')
    st.stop()

#loop the selected stock
st.write(f'You have selected total {str(len(selectedStock))} stocks and retrieve stock data with {selectedYear} years base.')
for i in range(len(selectedStock)):
    st.write('Stock', i+1, f' : {selectedStock[i]} - {co_name[selectedStock[i]]}')

# get adj. closing price in once, 2-years base from today
ed = datetime.today()
sd = datetime.now() - timedelta(days=selectedYear*365)
dailyPrice = yf.download(selectedStock,sd, ed)['Adj Close']
if '0016.HK' in dailyPrice.columns:
    dailyPrice.at['2022-06-14T00:00:00','0016.HK']=93.30

# calculation variables
dailyReturn = dailyPrice.pct_change()
covMatrixDaily = dailyReturn.cov()
rfr = 0.0283            #10 years US Treasury Yield
pf = build_portfolio(data=dailyPrice)
pf.risk_free_rate = rfr
ef = EfficientFrontier(pf.comp_mean_returns(freq=1), pf.comp_cov())

def pf_stock_weight(weights):
    stock_allocation = pd.merge(ind_list, weights, left_index=True, right_index=True)
    stock_allocation = pd.merge(name_list, stock_allocation, left_index=True, right_index=True)
    stock_allocation['Allocation'] = (stock_allocation['Allocation']*100).round(2).astype(str) + "%"
    st.write(stock_allocation)

def pf_performance_RtnRiskSharp (weights):
    stockAllocation = weights.squeeze()
    (expected_return, volatility, sharpe) = finquant.quants.annualised_portfolio_quantities(stockAllocation, dailyReturn.mean(), covMatrixDaily, risk_free_rate= rfr, freq=252)
    st.metric("Execpted Return", f"{str(round(expected_return *100,2))}% ")
    st.metric("Volatility", f"{str(round(volatility *100,2))}% ")
    st.metric("Sharpe Ratio", f"{str(round(sharpe *100,2))}")
    
def pf_plot_ind_weight(weights):
    industry_allocation = pd.merge(ind_list, weights, left_index=True, right_index=True)
    industry_allocation = industry_allocation.groupby(["Industry"]).sum()
    industry_allocation = industry_allocation.loc[lambda df: df['Allocation'] > 0.0001]
    #Plot the pie chart
    fig, ax = plt.subplots(figsize = (10,7))
    ax.pie(industry_allocation.Allocation, labels = industry_allocation.index, autopct='%1.1f%%')
    ax.legend(title = "Industry")
    ax.set_title('Portfolio Proportion of Industry ')
    pie = plt.show()
    st.pyplot(pie)

def pf_plot_stocks_weight(weights):
    fig, ax = plt.subplots(figsize = (10,7))
    ax.pie(weights.Allocation, labels = weights.index, autopct='%1.1f%%')
    ax.legend(title = "Industry")
    ax.set_title('Portfolio Proportion of Stock ')
    pie = plt.show()
    st.pyplot(pie)

def pf_info (weights):
    pf_performance_RtnRiskSharp(weights)
    pf_stock_weight(weights)
    pf_plot_stocks_weight(weights)
    pf_plot_ind_weight(weights)  

def plot_efficient_frontier (dailyPrice):
    st.set_option('deprecation.showPyplotGlobalUse', False)
    opt_w, opt_res = pf.mc_optimisation(num_trials=5000)
    pf.mc_plot_results()
    pf.ef_plot_efrontier()
    pf.ef.plot_optimal_portfolios()
    pf.plot_stocks()
    fig=plt.show()
    st.pyplot(fig)

def pf_A ():
        st.subheader("Portfolio A:")
        st.write("""##### Optimisation for Maximum Sharpe ratio""")
        pf_info(pf.ef_maximum_sharpe_ratio())

def pf_B ():
        st.subheader("Portfolio B:")
        st.write("""##### Optimisation for Minimum Volatility""")
        pf_info(ef.minimum_volatility())

def pf_C_highest_rtn_warning(weight,target_return):
        weights = pf.ef_efficient_return(target_return, verbose=True)
        stockAllocation = weights.squeeze()
        (expected_return, volatility, sharpe) = finquant.quants.annualised_portfolio_quantities(stockAllocation, dailyReturn.mean(), covMatrixDaily, risk_free_rate= rfr, freq=252)
        if target_return > expected_return + 0.0001 :
            st.warning(f"The highest expected return of selected stock is {round(expected_return*100,2)}%. The result is shown as below.")
            st.write(f"""##### Minimum Volatility for the Highest Return of {round(expected_return*100,2)}%""")
        else:
            st.write(f"""##### Minimum Volatility for Target Return of {target_return*100} %""")

def pf_C ():
        st.subheader("Portfolio C:")
        target_return = st.number_input('input the target return you want to achieve', min_value=None, max_value=None, value = 0.26)
        
        pf_C_highest_rtn_warning(pf.ef_efficient_return,target_return)
        pf_info(pf.ef_efficient_return(target_return, verbose=True))

def pf_C2 ():
        st.subheader("Portfolio C:")
        target_return = st.number_input('input the target return you want to compare', min_value=None, max_value=None, value = 0.26)
        
        pf_C_highest_rtn_warning(pf.ef_efficient_return,target_return)
        pf_info(pf.ef_efficient_return(target_return, verbose=True))

def pf_C3 ():
        st.subheader("Portfolio C:")
        target_return = st.number_input('input the target return you want to compare ', min_value=None, max_value=None, value = 0.26)

        pf_C_highest_rtn_warning(pf.ef_efficient_return,target_return)
        pf_info(pf.ef_efficient_return(target_return, verbose=True))

def pf_D_lowest_col_warning(weight, target_volatility):
        weights = pf.ef_efficient_volatility(target_volatility, verbose=True)
        stockAllocation = weights.squeeze()
        (expected_return, volatility, sharpe) = finquant.quants.annualised_portfolio_quantities(stockAllocation, dailyReturn.mean(), covMatrixDaily, risk_free_rate= rfr, freq=252)
        if target_volatility < volatility - 0.0001:
            st.warning(f"The lowest volatility of selected stock is {round(volatility*100,4)}%. The result is shown as below.")
            st.write(f"""##### Maximum Sharpe Ratio for the Lowest Volatility of {round(volatility*100,4)}%""")
        else:
            st.write(f"""##### Maximum Sharpe Ratio for Target Volatility of {target_volatility*100} %""")

def pf_D ():
        st.subheader("Portfolio D:")
        target_volatility = st.number_input('input the target volatility you want to achieve', min_value=None, max_value=None, value = 0.22)
        pf_D_lowest_col_warning(pf.ef_efficient_return(target_volatility, verbose=True),target_volatility)
        pf_info(pf.ef_efficient_volatility(target_volatility, verbose=True))

def pf_D2 ():
        st.subheader("Portfolio D:")
        target_volatility = st.number_input('input the target volatility you want to compare', min_value=None, max_value=None, value = 0.22)
        pf_D_lowest_col_warning(pf.ef_efficient_return(target_volatility, verbose=True),target_volatility)
        pf_info(pf.ef_efficient_volatility(target_volatility, verbose=True))

def pf_D3 ():
        st.subheader("Portfolio D:")
        target_volatility = st.number_input('input the target volatility you want to compare ', min_value=None, max_value=None, value = 0.22)
        pf_D_lowest_col_warning(pf.ef_efficient_return(target_volatility, verbose=True),target_volatility)
        pf_info(pf.ef_efficient_volatility(target_volatility, verbose=True))

def pf_design ():
        st.subheader("Your portfolio:")
        with st.form("my_form"):
            st.caption("The sum of entered weighting shall be 1.")
            my_allocation = np.array([])
            for tickerSymbol in selectedStock:
                t = st.number_input(f'Stock {tickerSymbol} -  {nameList[tickerSymbol]} weighting is')
                my_allocation = np.append(my_allocation,t)    
            submitted = st.form_submit_button("Submit")
        if submitted:
            my_allocation = pd.DataFrame(my_allocation,columns = ['Allocation'], index = selectedStock)
            if my_allocation['Allocation'].sum() == 1:
                pf_info (my_allocation)
            else:
                st.warning('The sum of entered weighting must be 1. ')

def pf_design2 ():
        st.subheader("Your portfolio:")
        with st.form("my_form2"):
            st.caption("The sum of entered weighting shall be 1.")
            my_allocation = np.array([])
            for tickerSymbol in selectedStock:
                t = st.number_input(f'Stock {tickerSymbol} -  {nameList[tickerSymbol]} weighting is')
                my_allocation = np.append(my_allocation,t)    
            submitted = st.form_submit_button("Submit")
        if submitted:
            my_allocation = pd.DataFrame(my_allocation,columns = ['Allocation'], index = selectedStock)
            if my_allocation['Allocation'].sum() == 1:
                pf_info (my_allocation)
            else:
                st.warning('The sum of entered weighting must be 1. ')

def portfolio_all_option (dailyPrice):
    colT1, colT2 = st.columns(2)
    with colT1:
        pf_A()
    with colT2:
        pf_B()
    st.write("""## Portfolio Performance by enter target return / target volatility""")
    st.caption("According to above efficient frontier result, you might also enter your target reutrn / target volatility to find the minimum volatility / the maximum Sharpe ratio of stock weighting")
    colT1, colT2 = st.columns(2)
    with colT1:
        pf_C()
    with colT2:
        pf_D()

def ind_stock_performance(tickerSymbol):
        yf_stock_daily = yf.download(tickerSymbol, sd, ed)      #all data from yfinance
        pf_stock_dailyPrice = pf.get_stock(tickerSymbol)        #daily price only
        
        st.write(f"""#### Stock {str(tickerSymbol)} - {nameList[tickerSymbol]} (Industry: {indList[tickerSymbol]})""")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Average Daily Returns", f"{round(yf_stock_daily['Adj Close'].pct_change().mean()*100,2)}% ")
        col2.metric("Average Yearly Return", f"{round(float(pf_stock_dailyPrice.expected_return)*100,2)}% ")
        col3.metric("Average Volatility", f"{round(float(pf_stock_dailyPrice.volatility)*100,2)}%")
        
        f'Stock {tickerSymbol} Daily Adj. close Price'
        st.line_chart(pf_stock_dailyPrice.data)
        
        f'Stock {tickerSymbol} Daily Volume'
        st.bar_chart(yf_stock_daily.Volume)
        
        f'Stock {tickerSymbol} Simple Return'
        st.line_chart(yf_stock_daily['Adj Close'].pct_change())
        
        'Band Moving Average'
        dis = pf.get_stock(tickerSymbol).data.copy(deep=True)
        spans = [10, 50, 100, 150, 200]
        ma = compute_ma(dis, ema, spans, plot=True)
        st.line_chart(ma)
        st.pyplot(plt.show())

def ind_stock_compare(tickerSymbol):
        yf_stock_daily = yf.download(tickerSymbol, sd, ed)      #all data from yfinance
        pf_stock_dailyPrice = pf.get_stock(tickerSymbol)        #daily price only
        
        st.write(f"""#### Stock {str(tickerSymbol)} - {nameList[tickerSymbol]} (Industry: {indList[tickerSymbol]})""")
        
        #col1, col2, col3 = st.columns(3)
        st.metric("Average Daily Returns", f"{round(yf_stock_daily['Adj Close'].pct_change().mean()*100,2)}% ")
        st.metric("Average Yearly Return", f"{round(float(pf_stock_dailyPrice.expected_return)*100,2)}% ")
        st.metric("Average Volatility", f"{round(float(pf_stock_dailyPrice.volatility)*100,2)}%")
        
        f'Stock {tickerSymbol} Adj. close Price'
        st.line_chart(pf_stock_dailyPrice.data)
        
        f'Stock {tickerSymbol} Daily Volume'
        st.bar_chart(yf_stock_daily.Volume)
        
        f'Stock {tickerSymbol} Simple Return'
        st.line_chart(yf_stock_daily['Adj Close'].pct_change())
        
        'Band Moving Average'
        dis = pf.get_stock(tickerSymbol).data.copy(deep=True)
        spans = [10, 50, 100, 150, 200]
        ma = compute_ma(dis, ema, spans, plot=True)
        st.line_chart(ma)
        st.pyplot(plt.show())

tab1, tab2 = st.tabs(["show each stock performance", "optimise the portfolio"])

with tab1:    
    st.write("""## All Stock Performance""")
    
    'Daily Adj. Closing Price of Stocks'
    st.line_chart(dailyPrice)

    'Cumulative Returns of Stocks'
    st.line_chart(pf.comp_cumulative_returns())

    'Daily percentage changes of Returns'
    st.line_chart(dailyReturn)

    'Correlation'
    corrMatrix = dailyReturn.corr().round(2)
    corrFig = px.imshow(corrMatrix, zmin = -1, zmax = 1, color_continuous_scale='rdylgn', text_auto=True)
    st.write(corrFig)
    
    st.write("""## """)
    st.write("""## Compare Stock Performance""")
    
    with st.form("compare_stock"):
        col1, col2 = st.columns(2)
        with col1:
            compare_stock1 = st.selectbox('Stock you want to compare:', selectedStock)
        with col2:
            compare_stock2 = st.selectbox('Stock you want to compare: ', selectedStock)
        submitted = st.form_submit_button("Submit")
    if submitted:
        col1, col2 = st.columns(2)
        with col1:
            ind_stock_compare(compare_stock1)
        with col2:
            ind_stock_compare(compare_stock2)

    st.write("""## """)
    st.write("""## Individual Stock Performance""")

    for tickerSymbol in selectedStock:
        ind_stock_performance(tickerSymbol)
        st.write("""# """)

with tab2:
    st.write("""## Efficient Frontier""")
    st.caption("Below is the efficient frontier simulated by Monte Carlo method.")
    st.caption("It shown how the allocation of selected stocks and the return can be obtained from the object portfolio.")
    plot_efficient_frontier(dailyPrice)
    
    st.write("""## Optimisation for portfolio""")
    st.caption("""
    Based on the above **Efficient Frontier**, the portfolio can be optimised for
    - Portflio A: maximum Sharpe ratio
    - Portflio B: minimum volatility
    - Portflio C: minimum volatility for entering target return
    - Portflio D: maximum Sharpe ratio for entering target volatility
    """)
    
    tab4, tab5 = st.tabs(["show all otimised portfolio","design your own portfolio"])
    with tab4:
        portfolio_all_option(dailyPrice)

    with tab5:
        st.write("""## Design your own portfolio """)
        st.caption("You might compare the performance of any two portfolio in below.")
        st.caption("In tag 'your portfolio', you might enter specific weighting for each stock and press submit button to check out the customize portfolio performance.")
        colT1, colT2 = st.columns(2)
        with colT1:
            tabA, tabB, tabC, tabD= st.tabs(['portfolio A','portfolio B','portfolio C','portfolio D'])
            with tabA:
                pf_A()
            with tabB:
                pf_B()
            with tabC:
                pf_C2()
            with tabD:
                pf_D2()
        with colT2:
            tabA, tabB, tabC, tabD, tabE = st.tabs(['Your Portfolio','Portfolio A','Portfolio B','Portfolio C','Portfolio D'])
            with tabB:
                pf_A()
            with tabC:
                pf_B()
            with tabD:
                pf_C3()
            with tabE:
                pf_D3()
            with tabA:
                pf_design2()

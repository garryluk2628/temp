import yfinance as yf
import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta


def main():
    st.set_page_config(
    page_title="Stock Selection Tools",
    page_icon="📈",
    layout="wide"
    )

    st.title("📈 Stock Selection Tools")
    st.caption("No ideas on selecting stocks for your portfolio? Here is the tool for you to choose stocks base on their performance and volatility. Latest stock data are retrieved from Yahoo! Finance.")

    method = st.selectbox("Choose your stock selection criteria",(
        'Highest Return', 
        'Lowest Volatility', 
        'Best Sharpe Ratio'))

    period = st.selectbox("Choose your observation period",(
        '1 Year', 
        '1 Month', 
        '1 Week'))

    number = st.slider("Choose the number of stocks for considerations", min_value=1, max_value=20, value=1, step=1)

    if st.button('Confirm choice') == False:
        st.stop()

    ## ------------------------------------------
    rfr = 0.0283  #10 years US Treasury Yield

    if period == "1 Year":
        days = 365
        trade_day = 250
        description = "(per this year)"
    elif period == "1 Month":
        days = 31
        trade_day = 21
        description = "(per this month)"
    elif period == "1 Week":
        days = 7
        trade_day = 5
        description = "(per this week)"

    dailyPrice = get_allprice(days)
    if "2022-06-14" in dailyPrice.index:
        dailyPrice.at['2022-06-14','0016.HK']=93.30
    Returns = cal_return(dailyPrice, trade_day)
    vols = cal_volatility(dailyPrice, trade_day)
    sharpe = cal_sharperatio(Returns, vols, rfr)
    assets = asset_table(Returns, vols, sharpe)
    ticketname = get_ticket(assets)
    present_table = reassign_table(assets, ticketname)

    if method == "Highest Return":
        topic = "Stock with the Highest Return"
        results = present_table.sort_values(by="Returns", ascending=False).head(number)
    elif method == "Lowest Volatility":
        topic = "Stock with the Lowest Volatility"
        results = present_table.sort_values(by="Volatility", ascending=True).head(number)
    elif method == "Best Sharpe Ratio":
        topic = "Stock with the Highest Sharpe Ratio"
        results = present_table.sort_values(by="Sharpe Ratio", ascending=False).head(number)

    beststockname = [results.index[0], results["Stock Name"][0]]
    beststockdata = get_beststock(beststockname, 365)

    ## ---------------------------------------- ##

    st.subheader("Today's Highlight - " + beststockname[0] + " " + beststockname[1])
    st.caption(f"{topic} {description}")
    col1, col2, col3 = st.columns(3)
    col1.metric(
        label="Last Price",
        value=f"{round(beststockdata['Close'].iat[-1], 2)}",
        delta=f"{(((beststockdata['Close'].iat[-1])-(beststockdata['Close'].iat[-2]))/(beststockdata['Close'].iat[-1])):,.2%}"
    )
    col2.metric(
        label="Volume",
        value=f"{beststockdata['Volume'].iat[-1]:,}",
        delta=f"{(((beststockdata['Volume'].iat[-1])-(beststockdata['Volume'].iat[-2]))/(beststockdata['Volume'].iat[-2])):,.2%}"
    )
    col3.metric(
        label="52 Week Range",
        value=f"{round(beststockdata['Close'].min(), 2)} - {round(beststockdata['Close'].max(), 2)}"
    )

    st.line_chart(data=beststockdata['Close'])

    st.subheader(f"Top {number} stocks with {method} {description}")
    st.write(results)


def get_allprice(day):
    stocks = ['0001.HK','0002.HK','0003.HK','0005.HK','0006.HK',
        '0011.HK','0012.HK','0016.HK','0017.HK','0027.HK',
        '0066.HK','0101.HK','0175.HK','0241.HK','0267.HK',
        '0288.HK','0291.HK','0316.HK','0386.HK','0388.HK',
        '0669.HK','0688.HK','0700.HK','0762.HK','0823.HK',
        '0857.HK','0868.HK','0881.HK','0883.HK','0939.HK',
        '0941.HK','0960.HK','0968.HK','0981.HK','0992.HK',
        '1038.HK','1044.HK','1093.HK','1109.HK','1113.HK',
        '1177.HK','1211.HK','1299.HK','1378.HK','1398.HK',
        '1810.HK','1876.HK','1928.HK','1997.HK','2007.HK',
        '2020.HK','2269.HK','2313.HK','2318.HK','2319.HK',
        '2331.HK','2382.HK','2388.HK','2628.HK','2688.HK',
        '3690.HK','3968.HK','3988.HK','6098.HK','6862.HK',
        '9618.HK','9633.HK','9988.HK','9999.HK']
    ed = datetime.today()
    sd = datetime.now() - timedelta(days=day)
    return yf.download(stocks,sd,ed)['Close']


def cal_return(dailyPrice, trade_day):
    dailyreturns = dailyPrice.pct_change() +1
    avrtotal = (dailyreturns.sum())/len(dailyreturns.dropna(axis=0, how='any'))
    return pow(avrtotal, trade_day) -1


def cal_volatility(dailyPrice, trade_day):
    daily_std = np.std(dailyPrice.pct_change())
    return daily_std * (trade_day ** 0.5)


def cal_sharperatio(returns, vols, rfr):
    return (returns - rfr)/vols


def asset_table(returns, vols, sharpe):
    assets = pd.concat([returns, vols, sharpe], axis=1) 
    assets.columns = ['Returns', 'Volatility', 'Sharpe Ratio']
    return assets


def get_ticket(assets):
    name_list = {
        '0001.HK': 'CKH HOLDINGS', '0002.HK': 'CLP HOLDINGS', 
        '0003.HK': 'HK & CHINA GAS', '0005.HK': 'HSBC HOLDINGS', 
        '0006.HK': 'POWER ASSETS', '0011.HK': 'HANG SENG BANK', 
        '0012.HK': 'HENDERSON LAND', '0016.HK': 'SHK PPT', 
        '0017.HK': 'NEW WORLD DEV', '0027.HK': 'GALAXY ENT', 
        '0066.HK': 'MTR CORPORATION', '0101.HK': 'HANG LUNG PPT', 
        '0175.HK': 'GEELY AUTO', '0241.HK': 'ALI HEALTH', 
        '0267.HK': 'CITIC', '0288.HK': 'WH GROUP', 
        '0291.HK': 'CHINA RES BEER', '0316.HK': 'OOIL', 
        '0386.HK': 'SINOPEC CORP', '0388.HK': 'HKEX', 
        '0669.HK': 'TECHTRONIC IND', '0688.HK': 'CHINA OVERSEAS', 
        '0700.HK': 'TENCENT', '0762.HK': 'CHINA UNICOM', 
        '0823.HK': 'LINK REIT', '0857.HK': 'PETROCHINA', 
        '0868.HK': 'XINYI GLASS', '0881.HK': 'ZHONGSHENG HLDG', 
        '0883.HK': 'CNOOC', '0939.HK': 'CCB', 
        '0941.HK': 'CHINA MOBILE', '0960.HK': 'LONGFOR GROUP', 
        '0968.HK': 'XINYI SOLAR', '0981.HK': 'SMIC', 
        '0992.HK': 'LENOVO GROUP', '1038.HK': 'CKI HOLDINGS', 
        '1044.HK': 'HENGAN INT L', '1093.HK': 'CSPC PHARMA', 
        '1109.HK': 'CHINA RES LAND', '1113.HK': 'CK ASSET', 
        '1177.HK': 'SINO BIOPHARM', '1211.HK': 'BYD COMPANY', 
        '1299.HK': 'AIA', '1378.HK': 'CHINAHONGQIAO', 
        '1398.HK': 'ICBC', '1810.HK': 'XIAOMI-W', 
        '1876.HK': 'BUD APAC', '1928.HK': 'SANDS CHINA LTD', 
        '1997.HK': 'WHARF REIC', '2007.HK': 'COUNTRY GARDEN', 
        '2020.HK': 'ANTA SPORTS', '2269.HK': 'WUXI BIO', 
        '2313.HK': 'SHENZHOU INTL', '2318.HK': 'PING AN', 
        '2319.HK': 'MENGNIU DAIRY', '2331.HK': 'LI NING', 
        '2382.HK': 'SUNNY OPTICAL', '2388.HK': 'BOC HONG KONG', 
        '2628.HK': 'CHINA LIFE', '2688.HK': 'ENN ENERGY', 
        '3690.HK': 'MEITUAN-W', '3968.HK': 'CM BANK', 
        '3988.HK': 'BANK OF CHINA', '6098.HK': 'CG SERVICES', 
        '6862.HK': 'HAIDILAO', '9618.HK': 'JD-SW', 
        '9633.HK': 'NONGFU SPRING', '9988.HK': 'BABA-SW', 
        '9999.HK': 'NTES-S'
    }
    ticketlist = []
    namelist = []
    for row in assets.index:
        ticketlist.append(row)
    for i in ticketlist:
        namelist.append(name_list[i])
    return namelist


def reassign_table(asset_table, ticketname):
    asset_table["Stock Name"] = ticketname
    cols = asset_table.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    asset_table = asset_table[cols] 
    return asset_table


def get_beststock(beststockname, day):
    stock = beststockname[0]
    ed = datetime.today()
    sd = datetime.now() - timedelta(days=day)
    return yf.download(stock,sd,ed)


if __name__ == "__main__":
    main()

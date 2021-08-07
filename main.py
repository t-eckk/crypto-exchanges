#%%
from ccxt.async_support.base.exchange import Exchange
from ccxt.base.errors import RequestTimeout
from pandas.core.frame import DataFrame
from connection import connect_exchange
import ccxt
import asyncio
import datetime as dt
import pandas as pd
import json
from typing import Dict, Any, List
import numpy as np


def eod_exchange(exchange: str):
    def connect_exchange():
        public, secret = fetch_keys()
        cfg = {'enableRateLimit': True, 'apiKey': public, 'secret': secret}
        return getattr(ccxt, exchange)(cfg)

    def fetch_keys() -> List:
        with open('keys.json', 'r') as file:
            file = json.load(file)
        return file[exchange]

    def file_name(file: str, date: str) -> str:
        return 'eod_' + file + '_' + exchange + '_' + date + '.csv'

    def previous_date(date: str) -> str:
        return (dt.date.fromisoformat(date) - dt.timedelta(1)).isoformat()

    def previous_file(file: str, date: str) -> DataFrame:
        path = './eod/' + exchange + '/' + file
        return pd.read_csv(path + file_name(previous_date(date)), index_col=0)

    def exchange_name(exchange: Exchange) -> str:
        return str(exchange.__str__)[str(exchange.__str__).index('ccxt')+5:str(exchange.__str__).index('(')]
    
    def fetch_data(exchange: Exchange, symbols: List[str]) -> Dict:
        if exchange_name(exchange) == 'ftx':
            ext = '/USDT'
        elif exchange_name(exchange) == 'binance':
            ext = 'USDT'
        

        pairs = [symbol + ext for symbol in symbols]
        try:
            fetch = exchange.fetch_tickers(pairs)
        except RequestTimeout:
            print('Request timed out, restarting...')
            fetch_data(exchange, symbols)
        else:
            data = []
            for symbol in symbols:
                try:
                    data.append([fetch[symbol + ext]['last'], 100 * float(fetch[symbol + ext]['info']['change24h'])])
                except KeyError:
                    data.append([1.0, 0.0])
            return np.array(data)

    def todays_balance():
        ex = connect_exchange()
        today = pd.DataFrame(ex.fetch_total_balance(), index = ['Quantity']).T
        today = today[today['Quantity'] >= 1e-6] 
        fetch = fetch_data(ex, list(today.index))
        today['Last'] = fetch[:,0]
        today['%Chg24h'] = fetch[:,1]
        today['Position'] = (today['Last'] * today['Quantity'])
        today.loc['Total'] = ['-', '-', '-', today['Position'].sum()]
        today['Position'] = today['Position'].apply(lambda x: '%.5f' %x)
        return today

    return todays_balance()

    def balance_usd():
        pass
# %%
(dt.date.fromisoformat('2021-08-06') - dt.timedelta(1)).isoformat()
# %%
eod_exchange('ftx')
# %%
df = pd.DataFrame(ftx.fetch_total_balance(), index = ['Quantity']).T
df
# %%


# %%
binance.fetch_ticker('BTCUSDT')
# %%
symbols = ['BTC/USD', 'FTT/USD']
[ftx.fetch_tickers(symbols)[symbol]['last'] for symbol in ftx.fetch_tickers(symbols)]
# %%

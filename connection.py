#%%
import ccxt.async_support as ccxt
import os 

def exchange_list():
    return ['ftx', 'binance']

def create_config(exchange: str = ''):
    if exchange.lower() in exchange_list():
        return {
            'enableRateLimit': True,
            'apiKey': os.getenv(exchange.lower() + '_api'),
            'secret': os.getenv(exchange.lower() + '_secret')
        }
    else:
        raise ValueError('You must enter a valid exchange. See exchange_list() for available exchanges.')

def connect_exchange(exchange: str = ''):
    cfg = create_config(exchange)
    #return eval('ccxt.' + exchange.lower())(cfg)
    if exchange == 'ftx':
        return ccxt.ftx(cfg)
    elif exchange == 'binance':
        return ccxt.binance(cfg)

def connect_exc(exchange):
    cfg = create_config(exchange)
    #return eval('ccxt.' + exchange.lower())(cfg)
    if exchange == 'ftx':
        return ccxt.ftx(cfg).__init__  


# %%

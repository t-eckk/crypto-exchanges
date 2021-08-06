#%%
from connection import connect_exchange
import ccxt.async_support as ccxt
import os

public = 'PVLrqZz9BL0-m3VbXSeMwqASwlKhrNDJgsknfXNt'
secret = 'LohdcrQM6-ayGbMnVas5331wJVrtvi8Pkgm69vkD'

ftx = ccxt.ftx({
    'enableRateLimit': False,
    'apiKey': public,
    'secret': secret
})
# %%
ftx.fetch_order_book()
# %%
ftx.fetch_account_positions('BTC/USDT')
# %%
ftx.fetch_total_balance()

# %%
os.environ.get('FTX_SECRET')
# %%
os.getenv('FTX_SECRET')
# %%

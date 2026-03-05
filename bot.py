import os
import time
from binance.client import Client

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

client = Client(API_KEY, API_SECRET)

SYMBOL = "SOLUSDT"

TAKE_PROFIT = 1.40
STOP_LOSS = 0.90

def get_price():
    ticker = client.get_symbol_ticker(symbol=SYMBOL)
    return float(ticker["price"])

def get_balance(asset):
    balance = client.get_asset_balance(asset)
    return float(balance["free"])

def buy():
    price = get_price()
    usdt = get_balance("USDT")
    quantity = round(usdt / price, 3)
    order = client.order_market_buy(symbol=SYMBOL, quantity=quantity)
    print("Comprado:", order)
    return price

def sell(quantity):
    order = client.order_market_sell(symbol=SYMBOL, quantity=quantity)
    print("Vendido:", order)

def run():
    entry_price = buy()
    quantity = get_balance("SOL")

    while True:
        price = get_price()

        if price >= entry_price * TAKE_PROFIT:
            sell(quantity)
            print("Lucro realizado")
            break

        if price <= entry_price * STOP_LOSS:
            sell(quantity)
            print("Stop loss executado")
            break

        time.sleep(30)

run()

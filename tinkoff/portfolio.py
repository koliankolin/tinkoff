from library.utils import get_data_by_ticker, find_stocks_to_buy
from library.utils import THRESHOLD_RATING_SELL
from tinkoff.orders import Order
from tinkoff.scanner import Scanner
from tinkoff.urls import API_URL
import random
import requests
import json
from tinkoff.tokens import BROCKER_ACC, HEADER_AUTH

random.seed(42)

def get_positions():
    res = requests.get(API_URL + '/portfolio', {'brokerAccountId': BROCKER_ACC}, headers={'Authorization': HEADER_AUTH})
    positions = json.loads(res.text)['payload']['positions']
    return [{position['ticker']: {'figi': position['figi'], 'lots': position['lots'], }} for position in positions]

def get_positions_to_sell():
    stocks_to_sell = []
    positions = get_positions()
    for position in positions:
        ticker = _get_ticker_from_position(position)
        rat_all, rat_other, rat_ma = get_data_by_ticker(ticker)
        if rat_all <= THRESHOLD_RATING_SELL and (rat_other <= THRESHOLD_RATING_SELL or rat_ma <= THRESHOLD_RATING_SELL):
            stocks_to_sell.append(position)

    return stocks_to_sell

def sell_positions_to_sell():
    positions = get_positions_to_sell()
    if len(positions) == 0:
        return False
    for position in positions:
        order = Order(position)
        ticker = _get_ticker_from_position(position)
        scanner = Scanner(ticker)
        sell_by_market = order.sell_by_market()
        if not sell_by_market:
            price = scanner.get_price() * 0.98
            sell_by_limit = order.sell_by_limit(price)
            if sell_by_limit:
                print(f'Stock {ticker} was sold by LIMIT by {price}')
        else:
            print(f'Stock {ticker} was sold by MARKET')
    return True

def get_balance_in_rub():
    res = requests.get(API_URL + '/portfolio/currencies', params={'brokerAccountId': BROCKER_ACC},
                       headers={'Authorization': HEADER_AUTH})
    currencies = json.loads(res.text)['payload']['currencies']
    for currency in currencies:
        if currency['currency'] == 'RUB':
            return currency['balance']


def compact_portfolio():
    balance = get_balance_in_rub()
    if balance < 1000:
        return False
    stocks = find_stocks_to_buy()
    share = balance // len(stocks) * 0.9
    for stock in random.sample(stocks, len(stocks)):
        ticker = _get_ticker_from_position(stock)
        scanner = Scanner(ticker)
        price = scanner.get_price()
        if price:
            price *= 1.02
        else:
            continue
        lots_to_buy = int(share // price)
        position = {ticker: {'figi': scanner.get_figi_by_ticker(), 'lots': lots_to_buy}}
        order = Order(position)
        buy_by_market = order.buy_by_market()
        if not buy_by_market:
            buy_by_limit = order.buy_by_limit(price)
            if buy_by_limit:
                print(f'Stock {ticker} was bought by LIMIT by {price}')
        else:
            print(f'Stock {ticker} was bought by MARKET')

def _get_ticker_from_position(position):
    return list(position.keys())[0]

def _get_figi_from_position(position):
    return list(position.values())[0]['figi']

def _get_lots_from_position(position):
    return list(position.values())[0]['lots']



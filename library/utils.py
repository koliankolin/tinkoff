from library.urls import RUSSIAN_URL
import requests
from library.request_jsons import get_json_by_ticker, get_json_all
import json
from constants import THRESHOLD_RATING_BUY, PERCENT_PROVE, THRESHOLD_RATING_SELL

def get_data_by_ticker(ticker):
    return json.loads(requests.api.post(RUSSIAN_URL, get_json_by_ticker(ticker)).text)['data'][0]['d']

def find_stocks_to_buy() -> list:
    res = requests.api.post(RUSSIAN_URL, get_json_all(up=0, limit=1000))
    stocks = json.loads(res.text)['data']
    stocks_to_buy = []
    for stock in stocks:
        data = stock['d']
        ticker, close_price, rat_all, rat_other, rat_ma = data
        if rat_all > THRESHOLD_RATING_BUY and (rat_other > THRESHOLD_RATING_BUY or rat_ma > THRESHOLD_RATING_BUY):
            stocks_to_buy.append({ticker: close_price * (1 + PERCENT_PROVE)})

    return stocks_to_buy

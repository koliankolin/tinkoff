from tinkoff.urls import API_URL
import requests
import json
from tinkoff.tokens import HEADER_AUTH

class Scanner:
    def __init__(self, ticker):
        self.ticker = ticker

    def get_price(self):
        figi = self.get_figi_by_ticker()
        if not figi:
            return None
        res = requests.get(API_URL + '/market/orderbook',
                           params={'figi': figi, 'depth': 5},
                           headers={'Authorization': HEADER_AUTH})
        return json.loads(res.text)['payload']['lastPrice']

    def get_figi_by_ticker(self):
        res = requests.get(API_URL + '/market/search/by-ticker',
                           params={'ticker': self.ticker},
                           headers={'Authorization': HEADER_AUTH})
        instruments = json.loads(res.text)['payload']['instruments']
        instrument = instruments[0] if len(instruments) != 0 else None
        if not instrument or instrument['currency'] != 'RUB':
            return None
        return instrument['figi']

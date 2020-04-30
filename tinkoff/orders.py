from tinkoff.urls import API_URL
import requests
import json
from tinkoff.constants import BROCKER_ACC, SELL, BUY, OK
from tinkoff.portfolio import get_positions


class Order:
    def __init__(self, ticker):
        self.position = get_positions()[ticker]

    def sell_by_market(self):
        return self._check_res(self._make_request_marker(SELL))

    def buy_by_market(self):
        return self._check_res(self._make_request_marker(BUY))

    def sell_by_limit(self, price):
        return self._check_res(self._make_request_limit(SELL, price))

    def buy_by_limit(self, price):
        return self._check_res(self._make_request_limit(BUY, price))

    def _make_request_marker(self, type_):
        if type_ not in (BUY, SELL):
            return
        return requests.post(API_URL + '/orders/market-order',
                             data={'lots': self.position['lots'], 'operation': type_},
                             params={'figi': self.position['figi'], 'brokerAccountId': BROCKER_ACC})

    def _make_request_limit(self, type_, price):
        if type_ not in (BUY, SELL):
            return
        return requests.post(API_URL + '/orders/market-order',
                             data={'lots': self.position['lots'], 'operation': type_, 'price': price},
                             params={'figi': self.position['figi'], 'brokerAccountId': BROCKER_ACC})

    @staticmethod
    def _check_res(res):
        if res.status_code == 200:
            return json.loads(res.text)['status'] == OK
        return False

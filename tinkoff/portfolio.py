from tinkoff.urls import API_URL
import requests
import json
from tinkoff.constants import BROCKER_ACC

class Portfolio:


    def get_positions(self):
        positions = json.loads(requests.get(API_URL + '/portfolio', {'brokerAccountId': BROCKER_ACC}))['payload']['positions']
        return [{position['ticker']: {'figi': position['figi'], 'lots': position['lots'], }} for position in positions]

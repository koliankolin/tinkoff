import tinkoff.portfolio as portfolio
from library.utils import find_stocks_to_buy
import random

def main():
    print(f'Portfolio before trading: {portfolio.get_positions()}')
    print(f'Positions to sell: {portfolio.get_positions_to_sell()}')
    print('Selling positions...')
    portfolio.sell_positions_to_sell()
    print('Start trading...')
    portfolio.compact_portfolio()
    print(f'Portfolio after trading: {portfolio.get_positions()}')


if __name__ == '__main__':
    main()
from alpaca.trading.client import TradingClient
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

import random
import string


class trader:
    def __init__(self):
        self.key = "XXX"
        self.secret = "XXX"
        self.trading_client = TradingClient(self.key, self.secret, paper=True)
        self.orders = 0

    def id_generator(self, size=7, chars=string.ascii_uppercase + string.digits):
        self.orders = self.orders + 1
        return "".join(random.choice(chars) for _ in range(size)) + str(self.orders)

    def money(self):
        money = self.trading_client.get_account().cash
        return money

    def buy(self, ticker, units):
        # preparing order
        print("ticker", ticker)
        market_order_data = MarketOrderRequest(
            symbol=ticker,
            qty=units,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY,
            client_order_id=self.id_generator(),
        )
        # Market order
        market_order = self.trading_client.submit_order(market_order_data)
        return market_order

    def sell(self, ticker, units=1):
        # preparing order
        market_order_data = MarketOrderRequest(
            symbol=ticker,
            qty=units,
            side=OrderSide.SELL,
            time_in_force=TimeInForce.DAY,
            client_order_id=self.id_generator(),
        )
        # Market order
        market_order = self.trading_client.submit_order(order_data=market_order_data)
        return market_order

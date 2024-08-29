from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import GetPortfolioHistoryRequest
from alpaca.common.enums import BaseURL
from typing import Optional, List, Union
from alpaca.trading.models import PortfolioHistory
from alpaca.common import RawData

import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dt

import random
import string
import time


class trader:
    def __init__(self):
        self.key = "XXX"
        self.secret = "XXXX"
        self.trading_client = TradingClient(self.key, self.secret)
        self.orders = 0
        self.cash = 0

    def open_positions(self):
        position = self.trading_client.get_all_positions()
        ticker_names = []
        for positions in position:
            ticker_names.append([positions.symbol, round(float(positions.qty), 2)])
        return ticker_names

    def id_generator(self, size=7, chars=string.ascii_uppercase + string.digits):
        self.orders = self.orders + 1
        return "".join(random.choice(chars) for _ in range(size)) + str(self.orders)

    def money(self):
        self.cash = self.trading_client.get_account().cash
        return self.cash

    def stock_value(self):
        stock_value = self.trading_client.get_account().portfolio_value
        stock_value = float(stock_value) - float(self.cash)
        return round(stock_value, 2)

    def buy(self, ticker, units):
        # preparing order
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

    def get_portfolio_history(
        self, filter: Optional[GetPortfolioHistoryRequest] = None
    ) -> Union[PortfolioHistory, RawData]:
        """
        Gets the portfolio history statistics.

        Args:
            filter (Optional[GetPortfolioHistoryRequest]): The parameters to filter the history with.

        Returns:
            PortfolioHistory: The portfolio history statistics for the account.
        """
        # checking to see if we specified at least one param
        params = filter.to_request_fields() if filter else {}

        response = self.trading_client.get("/account/portfolio/history", params)

        if self.trading_client._use_raw_data:
            return response

        return PortfolioHistory(**response)

    def visualise(self):
        portFilter = GetPortfolioHistoryRequest(
            extended_hours=True, period="1D", timeframe="1H"
        )
        portHistory = self.get_portfolio_history(filter=portFilter)

        # Convert timestamps to datetime objects
        dates = [dt.datetime.fromtimestamp(ts) for ts in portHistory.timestamp]
        datenums = md.date2num(dates)

        # Set up the figure size
        plt.figure(figsize=(10, 6))

        # Create the plot
        plt.plot(datenums, portHistory.equity, "r-", alpha=0.5)

        # Format the date axis
        ax = plt.gca()
        xfmt = md.DateFormatter("%H:%M")
        ax.xaxis.set_major_formatter(xfmt)

        # Set labels and title
        plt.xlabel("Time")
        plt.ylabel("Equity")
        plt.title(f'Portfolio Value on {dt.date.today().strftime("%b-%d-%Y")}')

        # Add a grid
        plt.grid(True)

        # Save the figure
        plt.savefig("Bot/static/graph.png", bbox_inches="tight")

        # Optionally show the plot if you're testing locally
        # plt.show()

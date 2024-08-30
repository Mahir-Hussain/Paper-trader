from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import GetPortfolioHistoryRequest
from typing import Optional, List, Union
from alpaca.trading.models import PortfolioHistory
from alpaca.common import RawData

import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dt

import random
import string
import requests


class trader:
    def __init__(self):
        self.key = ""
        self.secret = ""
        self.trading_client = TradingClient(self.key, self.secret)
        self.orders = 0

    def open_positions(self):
        position = self.trading_client.get_all_positions()
        ticker_names = []
        for positions in position:
            qty = round(float(positions.qty), 2)
            current_price = float(positions.current_price)
            ticker_names.append(
                [positions.symbol, qty, current_price, round(current_price * qty, 2)]
            )
        return ticker_names

    # ID is random but is appended with an incrementing value to show what run the software is on
    def id_generator(self, size=7, chars=string.ascii_uppercase + string.digits):
        self.orders = self.orders + 1
        return "".join(random.choice(chars) for _ in range(size)) + str(self.orders)

    def money(self):
        cash = self.trading_client.get_account().cash
        return cash

    def stock_value(self):
        stock_value = self.trading_client.get_account().portfolio_value
        stock_value = float(stock_value) - float(self.money())
        return round(stock_value, 2)

    # Checks if ticker is valid OR returns ticker from company name
    def get_ticker(self, company_name):
        yfinance = "https://query2.finance.yahoo.com/v1/finance/search"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        params = {"q": company_name, "quotes_count": 1, "country": "United Kingdom"}

        res = requests.get(
            url=yfinance, params=params, headers={"User-Agent": user_agent}
        )
        data = res.json()
        try:
            company_code = data["quotes"][0]["symbol"]
            return company_code
        except Exception:
            return False

    def buy(self, ticker, units=1):
        valid = self.get_ticker(ticker)
        if valid != False and float(units):
            # Preparing order
            market_order_data = MarketOrderRequest(
                symbol=valid,  # if user enters company name instead of ticker get_ticker will return ticker
                qty=float(units),
                side=OrderSide.BUY,
                time_in_force=TimeInForce.DAY,
                client_order_id=self.id_generator(),
            )
            # Market order
            try:
                market_order = self.trading_client.submit_order(market_order_data)
                return market_order.status
            except Exception as error:
                return error
        else:
            return "Either you entered invalid ticker or quantity"

    def sell(self, ticker, units=1):
        # Check if valid ticker
        valid = self.get_ticker(ticker)
        if valid != False and float(units):
            # preparing order
            market_order_data = MarketOrderRequest(
                symbol=valid,
                qty=float(units),
                side=OrderSide.SELL,
                time_in_force=TimeInForce.DAY,
                client_order_id=self.id_generator(),
            )
            # Market order
            try:
                market_order = self.trading_client.submit_order(market_order_data)
                return market_order.status
            except Exception as error:
                return error
        else:
            return "Either you entered invalid ticker or quantity"

    def get_portfolio_history(
        self, filter: Optional[GetPortfolioHistoryRequest] = None
    ) -> Union[PortfolioHistory, RawData]:
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

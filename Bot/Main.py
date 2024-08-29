from flask import Flask, request, render_template, Response
from tradingbot import trader

import io
import time


class webviewer:
    def __init__(self, host="192.168.0.17", port=5000):
        self.app = Flask(__name__, template_folder="templates", static_folder="static")
        self.host = host
        self.port = port
        # Handles trading component
        self.trader = trader()
        # Main page
        self.app.add_url_rule("/", "index", self.index)
        self.setup_routes()

    def setup_routes(self):

        @self.app.route("/buy-order", methods=["POST"])
        def buy():
            buy_stock = ""
            units = 1

            # Access the form data
            buy_stock = str(request.form.get("buy-stock"))
            units = float(request.form.get("quantity"))
            # Purchases amount, defualt is 1 share
            self.trader.buy(buy_stock, units)

            # Render the form with the submitted data (if any)
            return self.index()

        @self.app.route("/sell-order", methods=["POST"])
        def sell():
            sell_order = ""
            units = 1

            # Access the form data
            sell_order = str(request.form.get("sell-stock"))
            units = float(request.form.get("quantity"))
            # Purchases amount, defualt is 1 share
            self.trader.sell(sell_order, units)

            # Render the form with the submitted data (if any)
            return self.index()

    def index(self):
        return render_template(
            "index.html",
            money=self.trader.money(),
            stock_value=self.trader.stock_value(),
            tickers=self.trader.open_positions(),
        )

    def run(self):
        self.trader.visualise()
        time.sleep(5)
        self.app.run(host=self.host, port=self.port, debug=True)


webviewer().run()

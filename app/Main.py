from flask import Flask, request, render_template, flash, redirect
from tradingbot import trader


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

    # Setup route for buying and selling
    def setup_routes(self):
        @self.app.route("/execute-order", methods=["POST", "GET"])
        def execute():
            transaction = request.form.get("transaction")  # BUY or SELL
            stock = request.form.get("execute")  # Ticker symbol from form input
            units = request.form.get("quantity")  # Unit amount

            # Call the appropriate method based on transaction type
            if transaction == "BUY":
                return self.buy(stock, units)
            elif transaction == "SELL":
                return self.sell(stock, units)
            else:
                return redirect("/", code=302)

    def buy(self, buy_stock, units):
        order = self.trader.buy(buy_stock, units)

        if order == "OrderStatus.ACCEPTED":
            flash("Buy order sent.")
        elif order == "OrderStatus.PENDING_NEW":
            flash("Order pending")
        else:
            flash(f"An error occured - {order}")

        # Render the form again with a popup form above
        return self.index()

    def sell(self, sell_order, units):
        # sell_order = ""
        # units = 0

        # Access the form data
        # sell_order = str(request.form.get("EXECUTE-ID"))
        # units = request.form.get("quantity")

        # Purchases amount, defualt is 1 share
        order = self.trader.sell(sell_order, units)
        if str(order) == "OrderStatus.ACCEPTED":
            flash("Sell order sent.")
        elif str(order) == "OrderStatus.PENDING_NEW":
            flash("Order pending")
        else:
            flash(f"An error occured - {order}")

        # Render the form with the popup form above
        return self.index()

    def index(self):
        return render_template(
            "index.html",
            money=self.trader.money(),
            stock_value=self.trader.stock_value(),
            tickers=self.trader.open_positions(),
        )

    def run(self):
        self.trader.visualise()  # Makes the graph to be displayed
        self.app.run(host=self.host, port=self.port, debug=True)


webviewer().run()

from flask import Flask, request, render_template, flash, redirect
from tradingbot import trader


class webviewer:
    def __init__(self, host="192.168.0.17", port=5000):
        self.app = Flask(__name__, template_folder="templates", static_folder="static")
        self.app.secret_key = "super secret key"
        self.host = host
        self.port = port
        # Handles trading component
        self.trader = trader()
        # Main page
        self.app.add_url_rule("/", "index", self.index)
        self.setup_routes()

    # Handles main buying and selling
    def setup_routes(self):

        @self.app.route("/buy-order", methods=["POST", "GET"])
        def buy():
            if request.method == "POST":
                buy_stock = ""
                units = 0

                # Access the form data
                buy_stock = str(request.form.get("buy-stock"))
                units = request.form.get("quantity")
                # Purchases amount, defualt is 1 share
                order = self.trader.buy(buy_stock, units)

                if str(order) == "OrderStatus.ACCEPTED":
                    flash("Buy order sent.")
                elif str(order) == "OrderStatus.PENDING_NEW":
                    flash("Order pending")
                else:
                    flash(f"An error occured - {order}")

                # Render the form again with a popup form above
                return self.index()
            elif request.method == "GET":
                return redirect("/", code=302)

        @self.app.route("/sell-order", methods=["POST", "GET"])
        def sell():
            if request.method == "POST":
                sell_order = ""
                units = 0

                # Access the form data
                sell_order = str(request.form.get("sell-stock"))
                units = request.form.get("quantity")

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
            else:
                return redirect("/", code=302)

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

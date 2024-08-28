from alpaca.trading.client import TradingClient

class trader:
    def __init__(self):
        self.key = "XXX"
        self.secret = "XXX"
        self.trading_client = TradingClient(self.key, self.secret, paper=True)
    
    def money(self):
        money = self.trading_client.get_account().cash
        return money
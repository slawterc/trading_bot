from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime
import json

creds = open('CREDS.json')
ALPACA_CREDS = json.load(creds)

start_date = datetime(2023,12,15)
end_date = datetime(2023,12,31)
symbol = "SPY"
cash_at_risk = .5


class MLTrader(Strategy):
    def initialize(self, symbol:str=symbol, cash_at_risk:float=cash_at_risk):
        self.symbol = symbol
        self.sleeptime = "24H"
        self.last_trade = None
        self.cash_at_risk = cash_at_risk

    def postion_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price,0)
        return cash, last_price, quantity
    
    def on_trading_iteration(self):
        cash, last_price, quantity =  self.postion_sizing()

        if cash > last_price:
            if self.last_trade == None:
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "buy",
                    type="brackey",
                    take_profit_price=last_price*1.20,
                    stop_loss_price=last_price*.95
                )
                self.submit_order(order)
                self.last_trade = "buy" 



broker = Alpaca(ALPACA_CREDS)
strategy = MLTrader(name="mlstrat", broker=broker, parameters={"symbol":symbol, "cash_at_risk":cash_at_risk})

strategy.backtest(YahooDataBacktesting, start_date, end_date, parameters={"symbol":symbol, "cash_at_risk": cash_at_risk})
from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime
from timedelta import Timedelta
from ai_util import estimate_sentiment
from api_util import REST
from strategy_util import get_symbol_ticker_df, get_MACD_with_signals
import json

creds = open('ALPACA_CREDS.json')
ALPACA_CREDS = json.load(creds)

ALPACA ={
    "API_KEY":ALPACA_CREDS['API_KEY'],
    "API_SECRET":ALPACA_CREDS['API_SECRET'],
    "PAPER":True
}


symbol = "SPY"
cash_at_risk = .5


class MLTrader(Strategy):
    def initialize(self, symbol:str=symbol, cash_at_risk:float=cash_at_risk):
        self.symbol = symbol
        self.sleeptime = "5M"
        self.last_trade = None
        self.cash_at_risk = cash_at_risk
        self.api_util = REST(ALPACA_CREDS=ALPACA)

    def postion_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price,0)
        return cash, last_price, quantity
    
    def get_dates(self):
        today = self.get_datetime()
        three_days_prior = today - Timedelta(days=3)
        return today.strftime('%Y-%m-%d'), three_days_prior.strftime('%Y-%m-%d')

    
    def get_sentiment(self):
        end, start = self.get_dates()
        news = self.api_util.get_headlines(symbol=self.symbol, start=start, end=end)

        probability, sentiment = estimate_sentiment(news)
        return probability, sentiment
    
    def get_macd_signals(self):
        end, start = self.get_dates()
        df = get_symbol_ticker_df(symbol=self.symbol, start_date=start, end_date=end)
        signals_df = get_MACD_with_signals(df)
        if signals_df.empty:
            return 'Hold'
        else:
            lastrow=signals_df.iloc[-1]
            return lastrow['order']

    
    def on_trading_iteration(self):
        cash, last_price, quantity =  self.postion_sizing()
        probability, sentiment = self.get_sentiment()
        order_type = self.get_macd_signals()

        if cash > last_price:
            if order_type == 'Buy':
                if sentiment == "positive" and probability > .999: 
                    if self.last_trade == "sell": 
                        self.sell_all() 
                    order = self.create_order(
                        self.symbol, 
                        quantity, 
                        "buy", 
                        type="market"
                        # type="bracket", 
                        # take_profit_price=last_price*1.25, 
                        # stop_loss_price=last_price*.95
                    )
                    self.submit_order(order) 
                    self.last_trade = "buy"
                    order_type == ""
            elif order_type == 'Sell' and self.last_trade != None:
            #sentiment == "negative" and probability > .98: 
                if self.last_trade == "buy": 
                    self.sell_all() 
                order = self.create_order(
                    self.symbol, 
                    quantity, 
                    "sell", 
                    type="market"
                    # type="bracket", 
                    # take_profit_price=last_price*.8, 
                    # stop_loss_price=last_price*1.05
                )
                self.submit_order(order) 
                self.last_trade = "sell"
                order_type = ""


start_date = datetime(2024,6,20)
end_date = datetime(2024,6,30)
broker = Alpaca(ALPACA)
strategy = MLTrader(name="mlstrat", broker=broker, parameters={"symbol":symbol, "cash_at_risk":cash_at_risk})

strategy.backtest(YahooDataBacktesting, start_date, end_date, parameters={"symbol":symbol, "cash_at_risk": cash_at_risk})

# trader = Trader()
# trader.add_strategy(strategy)
# trader.run_all()
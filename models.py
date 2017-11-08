"""
Global Beverage Corporation Exchange - Super Simple Stock Market
"""


STOCK_FIELDS_LIST = ["Stock Symbol", "Type", "Last Dividend", "Fixed Dividend", "Par Value"]
TRADE_FIELDS_LIST = ["Timestamp", "Stock Symbol", "Quantity", "Buy/Sell", "Price"]


from datetime import datetime as dt, timedelta


# relevant formulas
def _dividend_yield_common(last_div, price):
    return last_div / price

def _dividend_yield_preferred(fixed_div, par_value, price):
    return fixed_div / 100 * par_value / price

def _pe_ratio(price, div):
    return price / div

def _geo_mean(stks_list):
    pro = stks_list[0]

    if len(stks_list) > 1:
        for s in stks_list[1:]:
            pro = pro * s
        
    return pro ** (1.0 / len(stks_list))

def _volume_weighted_stock_price(trades):
    if len(trades):
        return float('{p:.2f}'.format(p=sum(map(lambda x: x.Price * x.Quantity, trades)) \
                                      / sum(map(lambda x: x.Quantity, trades))))
    else:
        return None
    
    #raise RuntimeError("Unimplemented")
    #pass


class Stock:
    """
    A Stock represents a company stock in the Market, independent of trades.
    """
    def __init__(self):
        """Create a new stock object with placeholders."""
        for f in STOCK_FIELDS_LIST:
            setattr(self, f, None)

    def div_yield(self, price):
        """Alias for `dividend_yield`"""
        return self.dividend_yield(price)
    
    def dividend_yield(self, price):
        """Given a price, return the Dividend Yield of this stock."""
        if self.Type == "Common":
            return _dividend_yield_common(getattr(self, "Last Dividend"),
                                          price)
        else: # preferred
            return _dividend_yield_preferred(getattr(self, "Fixed Dividend"),
                                             getattr(self, "Par Value"),
                                             price)
        
    def pe_ratio(self, price):
        """Given a price, return the price-earnings ratio of this stock."""
        return _pe_ratio(price, getattr(self, "Last Dividend"))


    def volume_weighted_stock_price(self, market):
        """Given a market, return the Volume Weighted Stock Price based on trades in the past 5 minutes."""
        return market.volume_weighted_stock_price(symbol=getattr(self,"Stock Symbol"))
    
    
class Trade:
    """
    A Trade represents a purchase or sale of a quantity of stock at a certain price at a certain time.
    """
    def __init__(self):
        """Create a new buy or sell trade instruction."""
        for f in TRADE_FIELDS_LIST:
            setattr(self, f, None)

    def validate(self):
        """Ensure there is valid content in all the fields of this Trade."""
        for f in TRADE_FIELDS_LIST:
            if getattr(self,f,None) is None:
                return False

        return True

class Market:
    """
    The Market object manages the list of Stocks and Trades.
    """
    def __init__(self):
        """Create the stock market with a placeholder list for the Stocks & Trades."""
        self.stocks = []
        self.trades = []

    def add_stock(self, stock):
        """Add a new Stock to the exchange."""
        symbol = getattr(stock, "Stock Symbol", None)

        if not bool(symbol):
            raise RuntimeError("A new Stock must have a unique Stock Symbol to be added to the exchange.")
        
        if bool(len(list(filter(lambda x: getattr(x, "Stock Symbol", "") == symbol, self.stocks)))):
            raise RuntimeError("A stock with symbol {} already exists in the exchange.".format(symbol))

        self.stocks.append(stock)
        return True

    def get_stock(self, symbol):
        """Retrieve a Stock object from the exchange."""
        match = list(filter(lambda x: getattr(x, "Stock Symbol") == symbol, self.stocks))
        if match:
            return match[0]
        else:
            return None
        
    def add_trade(self, trade):
        """Record a new Trade on the exchange."""

        if not trade.Timestamp:
            trade.Timestamp = dt.utcnow()

        if not trade.validate():
            raise RuntimeError("Cannot add an incomplete Trade to the exchange.")

        # a trade must be for a stock on our exchange
        symb = getattr(trade, "Stock Symbol")
        if not self.get_stock(symb):
            raise RuntimeError("Cannot add a Trade for unknown Stock Symbol {}".format(symb))
        
        self.trades.append(trade)
        return True

    
    def volume_weighted_stock_price(self, symbol=None):
        """Given a stock symbol, return the volume-weighted price for that stock in the past 5 minutes."""
        stock = self.get_stock(symbol)

        if not stock:
            raise RuntimeError("Cannot calculate Volume Weighted Stock Price for non-existent stock {}".\
                               format(symbol))

        if symbol:
            relevant_trades = list(filter(lambda x: getattr(x, "Stock Symbol") == symbol \
                                          and dt.utcnow() - x.Timestamp <= timedelta(minutes=5),
                                          self.trades))
        else:
            relevant_trades = self.trades

        try:
            return _volume_weighted_stock_price(relevant_trades)
        except TypeError:
            return 0

    
    def all_share_index(self):
        """Return the All Share Index for GBCE."""
        if len(self.stocks):
            return _geo_mean(list(filter(lambda x: x is not None,
                                         map(lambda x: x.volume_weighted_stock_price(self),
                                             self.stocks))))
        else:
            return float(0)

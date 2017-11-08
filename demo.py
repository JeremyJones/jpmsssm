
from random import choice
from time import sleep
from models import Market, Stock, Trade
from data import SAMPLE_DATA

def main():
    """
    Application that will...
    """
    gbce = Market()

    # open the market
    print("------------------------------------")
    print("Global Beverage Corporation Exchange")
    print("------------------------------------")


    # load sample stock data into the market
    for stock in SAMPLE_DATA:
        stk = Stock()
        setattr(stk, "Stock Symbol", stock[0])
        setattr(stk, "Type", stock[1])
        setattr(stk, "Last Dividend", stock[2])
        setattr(stk, "Fixed Dividend", stock[3])
        setattr(stk, "Par Value", stock[4])

        gbce.add_stock(stk)
        print("Welcome {} to the GBCE".format(getattr(stk, "Stock Symbol")))
        sleep(0.8)

        
    # run some trades
    for trade_no in range(20):
        t = Trade()
        setattr(t, "Stock Symbol", choice(list(map(lambda x: x[0], SAMPLE_DATA))))
        setattr(t, "Buy/Sell", choice(['Buy','Sell']))
        setattr(t, "Quantity", choice([500,1000,2000,5000,10000,20000,50000]))
        setattr(t, "Price", choice(list(range(50,150))))

        gbce.add_trade(t)

        sto = gbce.get_stock(getattr(t,"Stock Symbol"))

        print("{sale_report} ({all_share})".\
              format(sale_report="{time}: {b} {q} shares of {s} for {p}".\
                     format(b=getattr(t,"Buy/Sell"),
                            time=t.Timestamp.time().replace(microsecond=0),
                            q=t.Quantity,p=t.Price,
                            s=getattr(t,"Stock Symbol")),
                     all_share="GBCE All-Share: {a:.2f}".\
                     format(a=gbce.all_share_index())))
        
        sleep(0.75 + choice([0.10,0.15,0.25,0.45]))


    # close the market
    print("------------------------------------")
        

if __name__ == "__main__":
    main()

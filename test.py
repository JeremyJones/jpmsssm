import unittest
import models as gbce
from random import choice
from data import SAMPLE_DATA

class MarketTestCase(unittest.TestCase):
    def setUp(self):
        self.me = gbce.Market()

    def test_market_object(self):
        self.assertIsInstance(self.me, gbce.Market)

    def test_empty_market_list(self):
        self.assertEqual(len(self.me.stocks), 0)

    def test_add_blank_stock_to_exchange(self):
        stk = gbce.Stock()
        self.assertRaises(RuntimeError, self.me.add_stock, stk)
        
    def test_add_stock_to_exchange(self):
        stk = gbce.Stock()
        setattr(stk, "Stock Symbol", "7UP")
        setattr(stk, "Type", "Common")
        setattr(stk, "Par Value", 100)
        
        self.assertTrue(self.me.add_stock(stk))

    def test_add_duplicate_to_exchange(self):
        stk = gbce.Stock()
        setattr(stk, "Stock Symbol", "7UP")
        setattr(stk, "Type", "Common")
        setattr(stk, "Par Value", 100)
        
        self.me.add_stock(stk)

        stk = gbce.Stock()
        setattr(stk, "Stock Symbol", "7UP")
        setattr(stk, "Type", "Common")
        setattr(stk, "Par Value", 100)

        self.assertRaises(RuntimeError, self.me.add_stock, stk)


    def test_get_stock_ok(self):
        stk = gbce.Stock()
        setattr(stk, "Stock Symbol", "7UP")
        setattr(stk, "Type", "Common")
        setattr(stk, "Par Value", 100)
        self.me.add_stock(stk)

        self.assertIsNotNone(self.me.get_stock("7UP"))
        
    def test_get_stock_not_ok(self):
        stk = gbce.Stock()
        setattr(stk, "Stock Symbol", "7UP")
        setattr(stk, "Type", "Common")
        setattr(stk, "Par Value", 100)
        self.me.add_stock(stk)

        self.assertIsNone(self.me.get_stock("FOO"))
        
        
    def test_geometric_mean__zero(self):
        self.assertEqual(0, self.me.all_share_index())

    def test_add_blank_trade_to_exchange(self):
        t = gbce.Trade()
        self.assertRaises(RuntimeError, self.me.add_trade, t)

        
    def test_add_unknown_trade_to_exchange(self):
        tra = gbce.Trade()
        tra.Quantity = 1000
        tra.Price = 203
        setattr(tra, "Stock Symbol", "ABC")
        setattr(tra, "Buy/Sell", "Buy")
        
        self.assertRaises(RuntimeError, self.me.add_trade, tra)

    def _get_stock(self):
        stk = gbce.Stock()
        setattr(stk, "Stock Symbol", "7UP")
        setattr(stk, "Type", "Common")
        setattr(stk, "Par Value", 100)
        return stk

    def _get_trade(self):
        tra = gbce.Trade()
        tra.Price = 1003
        tra.Quantity = 1000
        setattr(tra, "Stock Symbol", "7UP")
        setattr(tra, "Buy/Sell", "Sell")
        return tra

    def test_add_trade_to_exchange(self):
        stk = self._get_stock()
        self.me.add_stock(stk)
        tra = self._get_trade()
        self.assertTrue(self.me.add_trade(tra))

    def test_volume_weighted_stock_price(self):
        stk = self._get_stock()
        self.me.add_stock(stk)
        tra = self._get_trade()
        self.me.add_trade(tra)
        self.assertTrue(stk.volume_weighted_stock_price(self.me) > 0)
                
    def test_all_share_index(self):
        stk = self._get_stock()
        self.me.add_stock(stk)
        tra = self._get_trade()
        self.me.add_trade(tra)
        self.assertTrue(self.me.all_share_index() > 0)
        
    def tearDown(self):
        self.me = None


class StockTestCase(unittest.TestCase):
    def setUp(self):
        self.me = gbce.Stock()

    def test_stock_object(self):
        self.assertIsInstance(self.me, gbce.Stock)

    def test_empty_stock_object(self):
        for f in gbce.STOCK_FIELDS_LIST:
            self.assertIsNone(getattr(self.me, f))

    def test_get_set_symbol(self):
        for s in ['TEA','POP','ALE','GIN','JOE']:
            setattr(self.me, "Stock Symbol", s)
            self.assertEqual(getattr(self.me, "Stock Symbol"), s)
            
    def test_get_set_type(self):
        for s in ['Common','Preferred']:
            setattr(self.me, "Type", s)
            self.assertEqual(getattr(self.me, "Type"), s)
            
    def test_get_set_last_dividend(self):
        for s in [0,8,23,8,13]:
            setattr(self.me, "Last Dividend", s)
            self.assertEqual(getattr(self.me, "Last Dividend"), s)

    def test_get_set_fixed_dividend(self):
        for s in [1,8,23,8,13,None]:
            setattr(self.me, "Fixed Dividend", s)
            self.assertEqual(getattr(self.me, "Fixed Dividend"), s)

    def test_get_set_par_value(self):
        for s in [100,100,60,100,250]:
            setattr(self.me, "Par Value", s)
            self.assertEqual(getattr(self.me, "Par Value"), s)

    def test_div_yield_common(self):
        setattr(self.me, "Type", "Common")

        for dividend in [8,23,13]:
            setattr(self.me, "Last Dividend", dividend)

            for price in [6,123,4578]:
                self.assertEqual(getattr(self.me, "Last Dividend") / price,
                                 self.me.div_yield(price))

    def test_div_yield_preferred(self):
        setattr(self.me, "Type", "Preferred")

        for dividend in range(2,20):
            setattr(self.me, "Fixed Dividend", dividend)
            
            for par_value in [100,60,250]:
                setattr(self.me, "Par Value", par_value)

                for price in [32,45,135,5676]:
                    self.assertEqual(self.me.div_yield(price),
                                     dividend / 100 * par_value / price)
                                     
    def test_pe_ratio(self):
        for div in [8,23,8,13]:
            setattr(self.me, "Last Dividend", div)

            for price in [635,12323,432,3478,2,56]:
                self.assertEqual(self.me.pe_ratio(price),
                                 price / div)

    def tearDown(self):
        self.me = None






class ApplicationTestCase(unittest.TestCase):
    def setUp(self):
        """Application end-to-end test"""
        self.Market = gbce.Market()
        pass
    
    def test_requirement_2_a_i(self):
        """For a given stock, calculate the dividend yield."""

        stk = gbce.Stock()

        satr = setattr # shortcut

        # common
        satr(stk, "Stock Symbol", "POP")
        satr(stk, "Type", "Common")
        satr(stk, "Last Dividend", 8)

        dy = stk.dividend_yield(250)
        self.assertEqual(8/250, dy)

        # preferred
        satr(stk, "Stock Symbol", "GIN")
        satr(stk, "Type", "Preferred")
        satr(stk, "Fixed Dividend", 2)
        satr(stk, "Par Value", 100)

        dy = stk.dividend_yield(402)
        self.assertEqual(2/100*100/402, dy)

    def test_requirement_2_a_ii(self):
        """For a given stock, calculate the p/e ratio."""

        stk = gbce.Stock()
        setattr(stk, "Last Dividend", 23)

        for iter in range(100):
            price = choice(range(1,1000))
            pe = stk.pe_ratio(price)
            self.assertEqual(price/getattr(stk,"Last Dividend",1),
                             stk.pe_ratio(price))

    def test_requirement_2_a_iii(self):
        """For a given stock, record a trade, with timestamp, quantity, buy or sell indicator and price."""
        stk = gbce.Stock()

        satr = setattr # shortcut
        satr(stk, "Stock Symbol", "GIN")
        satr(stk, "Type", "Preferred")
        satr(stk, "Fixed Dividend", 2)
        satr(stk, "Par Value", 100)

        self.Market.add_stock(stk)

        t = gbce.Trade()
        setattr(t, "Stock Symbol", "GIN")
        setattr(t, "Buy/Sell", 'Buy')
        setattr(t, "Quantity", 1000)
        setattr(t, "Price", 114)
        self.Market.add_trade(t) # adds Timestamp

        self.assertTrue(len(self.Market.trades) > 0)

        # verify timestamp added ok
        self.assertIsNotNone(self.Market.trades[0].Timestamp)

    def test_requirement_2_a_iv(self):
        """For a given stock, calculate Volume Weighted Stock Price based on trades in past five minutes."""
        stk = gbce.Stock()

        satr = setattr # shortcut
        satr(stk, "Stock Symbol", "GIN")
        satr(stk, "Type", "Preferred")
        satr(stk, "Fixed Dividend", 2)
        satr(stk, "Par Value", 100)
        self.Market.add_stock(stk)

        t = gbce.Trade()
        setattr(t, "Stock Symbol", "GIN")
        setattr(t, "Buy/Sell", 'Buy')
        setattr(t, "Quantity", 1000)
        setattr(t, "Price", 114)
        self.Market.add_trade(t)

        self.assertTrue(self.Market.get_stock("GIN").\
                        volume_weighted_stock_price(self.Market) > 0.0)

    def test_requirement_2_b(self):
        """Calculate the GBCE All Share Index using teh geometric mean of the
        Volume Weighted Stock Price for all stocks."""

        for stock in SAMPLE_DATA:
            stk = gbce.Stock()
            setattr(stk, "Stock Symbol", stock[0])
            setattr(stk, "Type", stock[1])
            setattr(stk, "Last Dividend", stock[2])
            setattr(stk, "Fixed Dividend", stock[3])
            setattr(stk, "Par Value", stock[4])
            self.Market.add_stock(stk)

        for trade_no in range(1000):
            t = gbce.Trade()
            setattr(t, "Stock Symbol", choice(list(map(lambda x: x[0], SAMPLE_DATA))))
            setattr(t, "Buy/Sell", choice(['Buy','Sell']))
            setattr(t, "Quantity", choice(list(range(100,200))))
            setattr(t, "Price", choice(list(range(400,475))))
            self.Market.add_trade(t)
        
        self.assertTrue(self.Market.all_share_index() > 400 and \
                        self.Market.all_share_index() < 475)


if __name__ == "__main__":
    unittest.main()

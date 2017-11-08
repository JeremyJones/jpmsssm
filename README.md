# Super Simple Stock Market

## Description

Technical coding task, Jeremy Jones, November 2017.

## Synopsis

The core object model key deliverable is located in the file models.py:

    $ pydoc ./models.py
    Help on module models:

    NAME
        models - Global Beverage Corporation Exchange - Super Simple Stock Market

    CLASSES
        builtins.object
            Market
            Stock
            Trade
    ...

## Requirements

The file `test.py` contains a suite of tests corresponding to each
specific requirement:

    $ pydoc ./test.py

    
    Help on module test:
    
    NAME
        test
    
    CLASSES
        unittest.case.TestCase(builtins.object)
            ApplicationTestCase
            MarketTestCase
            StockTestCase
        
    ...

     |  Methods defined here:
     |  
     |  setUp(self)
     |      Application end-to-end test
     |  
     |  test_requirement_2_a_i(self)
     |      For a given stock, calculate the dividend yield.
     |  
     |  test_requirement_2_a_ii(self)
     |      For a given stock, calculate the p/e ratio.
     |  
     |  test_requirement_2_a_iii(self)
     |      For a given stock, record a trade, with timestamp, quantity, buy or sell indicator and price.
     |  
     |  test_requirement_2_a_iv(self)
     |      For a given stock, calculate Volume Weighted Stock Price based on trades in past five minutes.
     |  
     |  test_requirement_2_b(self)
     |      Calculate the GBCE All Share Index using teh geometric mean of the
     |      Volume Weighted Stock Price for all stocks.
     |  

and run directly:

     $ python ./test.py

     ............................
     ----------------------------------------------------------------------
     Ran 28 tests in 0.040s
     
     OK

     $

## Demonstration

The file `demo.py` contains a script which uses `models.py` and the sample data provided:

    $ python ./demo.py
    ------------------------------------
    Global Beverage Corporation Exchange
    ------------------------------------
    Welcome TEA to the GBCE
    Welcome POP to the GBCE
    Welcome ALE to the GBCE
    Welcome GIN to the GBCE
    Welcome JOE to the GBCE
    13:49:18: Sell 50000 shares of ALE for 113 (GBCE All-Share: 113.00)
    13:49:19: Sell 50000 shares of POP for 81 (GBCE All-Share: 95.67)
    13:49:20: Sell 50000 shares of TEA for 94 (GBCE All-Share: 95.11)
    13:49:21: Sell 10000 shares of POP for 80 (GBCE All-Share: 95.04)
    13:49:22: Sell 1000 shares of ALE for 74 (GBCE All-Share: 94.83)
    13:49:23: Buy 50000 shares of GIN for 98 (GBCE All-Share: 95.61)
    13:49:24: Buy 500 shares of JOE for 53 (GBCE All-Share: 84.97)
    13:49:25: Buy 2000 shares of GIN for 59 (GBCE All-Share: 84.71)
    13:49:26: Buy 10000 shares of TEA for 98 (GBCE All-Share: 84.83)
    13:49:27: Sell 2000 shares of TEA for 109 (GBCE All-Share: 84.91)
    13:49:28: Sell 2000 shares of POP for 99 (GBCE All-Share: 85.04)
    13:49:29: Sell 500 shares of TEA for 139 (GBCE All-Share: 85.10)
    13:49:30: Buy 2000 shares of ALE for 149 (GBCE All-Share: 85.31)
    13:49:31: Buy 10000 shares of JOE for 56 (GBCE All-Share: 86.21)
    13:49:32: Sell 1000 shares of POP for 112 (GBCE All-Share: 86.31)
    13:49:33: Buy 1000 shares of TEA for 135 (GBCE All-Share: 86.42)
    13:49:34: Buy 50000 shares of GIN for 121 (GBCE All-Share: 88.47)
    13:49:35: Sell 2000 shares of JOE for 93 (GBCE All-Share: 90.28)
    13:49:36: Buy 5000 shares of JOE for 59 (GBCE All-Share: 90.04)
    13:49:37: Buy 1000 shares of TEA for 53 (GBCE All-Share: 89.92)
    ------------------------------------
    $ 

## Assumptions

* Python 3

## Notes

The format specifier .02f is used for rounding.

## Navigating the Repository

This repository contains:

* README.md - this file
* models.py - **primary object code**
* demo.py - demonstration script
* test.py - unittest script

For additional support contact:

* https://www.linkedin.com/in/jerjones/

## Commentary

This section contains a description of major steps and the thinking
behind key decisions.

I began with gbce_test.py and gbce.py, setting up initial tests,
methods & data. Objects for a Stock and for a Trade and tests to
verify the formulas supplied are being used correctly. Object for
Market as an overall container and one expectedFailure for now to
allow me to move on and come back to that.

Added methods and tests for adding shares to the exchange and trades
of those shares.

Created the ApplicationTestCase for high-level deliverables.

Worked on requirement 2-a-i and (quickly) completed the successful
test for that. Added a random_trade function stub.

Added the Volume Weighted Stock Price code from the stub and the
corresponding revision to the tests. Re-worked existing code into
models.py and created gbce.py which loads the sample data, runs some
random trades and prints the all-share index after each trade.

Revised tests, added test_all_share_index and
test_volume_weighted_stock_price. Renamed files to README.md,
models.py, test.py and demo.py for clarity & simplicity.

Added remaining deliverable tests. Created the data.py file for the
last one, moving that SAMPLE_DATA out of demo.py.

Ongoing updates to the README & pydoc, refine, repeat, commit and
upload.

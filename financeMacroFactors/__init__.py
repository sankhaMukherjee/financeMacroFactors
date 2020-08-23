'''Macro Factors that affect stock prices

This Library provides a set of utilities for calculating
macro factors that is useful for evaluating whether a 
company is going to be profitable or not. There are
factors that decide that. This library will evolve over time
to be able to provide a number of utilities that will ultimately
allow individuals to generate insights that can be used for 
generating trading strategies.

Currently the following items are supported:

1. Data Download (``financeMacroFactors.companies``)
    1.1. Downloading fundamental data of a company from MarketWatch
    1.2. Downloading stock data from Yahoo! Finance
2. Calculate a companies valuation (``financeMacroFactors.valuation``)
    2.1. The P/S Valuation method
    2.2. The P/E Valuation method
    2.3. The DFE Valuation method
    2.4. The DCF Valuation method
'''

from financeMacroFactors.financeMacroFactors import sayHello
from financeMacroFactors import companies
from financeMacroFactors import valuation

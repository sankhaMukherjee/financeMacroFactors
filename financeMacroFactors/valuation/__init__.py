'''API for getting the valuation of a company

This module can be used for calculating the valuation of
a company. There are 4 different methods available for 
company valuation. These are the following:

1. The P/S Valuation method
2. The P/E Valuation method
3. The DFE Valuation method
4. The DCF Valuation method

For a detailed description of the different valuation methods
it may be helpful to look at the following Medium Article:

`Sure you know the stock price. But do you 
know its value? <https://medium.com/@sankha.mukherjee_007/sure-you-know-the-stock-price-but-do-you-know-its-value-65ab44dadd04>`_.


'''

from financeMacroFactors.valuation.valuationMethods import discountedFutureEarnings
from financeMacroFactors.valuation.valuationMethods import discountedCashFlow


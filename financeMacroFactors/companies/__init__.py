'''API for getting information about companies

This module can be used for obtaining a host of information for different
companies. This includes, information lists of companies that are part of
the S&P500, and other lists, and also about getting theri fundamental
information. This set of functions largely rely upon obtaining data from 
open sources.

'''

from financeMacroFactors.companies.companyLists import getSNP500CompanyList

from financeMacroFactors.companies.marketWarchData import getTickerFundamentalDataMW
from financeMacroFactors.companies.marketWarchData import extractYearlyData
from financeMacroFactors.companies.marketWarchData import extractQuarterlyData


from financeMacroFactors.companies.yahooData import getStockDataYahoo

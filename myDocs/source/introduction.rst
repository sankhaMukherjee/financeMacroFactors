Introduction
============

This library generates provides a set of convenience functions that will allow one to
generate macro economic factors and company financials within a single library. This
lirbary is intended to be used by value-investors who wish to create algorithmic investing
platforms that leverage free/paid data sources for their resource.

TLDR
----

For getting started, just install the library using PIP like any other library, and start using it. For example,
for getting a set of companies that are a part of the SNP 500 companies,

>>> import financeMacroFactors as fM 
>>> companies = fM.companies.getSNP500CompanyList()
>>> len(companies)
505
>>> import pprint
>>> pprint.pprint(companies[0])
{'CIK': '0000066740',
 'Date first added': '1976-08-09',
 'Founded': '1902',
 'GICS Sector': 'Industrials',
 'GICS Sub Industry': 'Industrial Conglomerates',
 'Headquarters Location': 'St. Paul, Minnesota',
 'SEC filings': 'reports',
 'Security': '3M Company',
 'Symbol': 'MMM'}
>>> 



Logging and Debugging
---------------------

Funcitons within the library use the term `financeMacroFactors` as the name upon which a standard python
logger can be used. Each function will log information to various levels of verbosity that can be used 
within your own implementations. Here is an example of obtaining debug information using the python 
logging favility from within the loggers:


>>> import logging 
>>> logger = logging.getLogger('financeMacroFactors') 
>>> logger.setLevel(logging.DEBUG) 
>>> ch = logging.StreamHandler()       
>>> ch.setLevel(logging.DEBUG)  
>>> formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
>>> ch.setFormatter(formatter)        
>>> logger.addHandler(ch)   
>>>
>>> import financeMacroFactors as fM 
>>> _ = fM.companies.getSNP500CompanyList()
2020-07-25 00:36:13,029 - financeMacroFactors.companies.companyLists.getSNP500CompanyList - DEBUG - Downloading data from the wikipedia page ...
2020-07-25 00:36:13,067 - financeMacroFactors.companies.companyLists.getSNP500CompanyList - DEBUG - Parsing the web data...
2020-07-25 00:36:13,413 - financeMacroFactors.companies.companyLists.getSNP500CompanyList - DEBUG - 505 rows of data generated ...
>>> 

On the other hand, it is possible to make sure that only the error level information is logged. For example,
the following code will only generate logging information when an error occurs, and be silent when the function
returns successfully.

>>> import logging 
>>> logger = logging.getLogger('financeMacroFactors') 
>>> logger.setLevel(logging.ERROR) 
>>> ch = logging.StreamHandler()       
>>> ch.setLevel(logging.ERROR)  
>>> formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
>>> ch.setFormatter(formatter)        
>>> logger.addHandler(ch)   
>>>
>>> import financeMacroFactors as fM 
>>> _ = fM.companies.getSNP500CompanyList()
>>> 


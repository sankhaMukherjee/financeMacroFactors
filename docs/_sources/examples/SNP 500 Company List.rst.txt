SNP 500 Company List
====================

An example of obtaining a list of companies that are in the SNP500.
The companies are obtained from the `wikipedia article
<https://en.wikipedia.org/wiki/List_of_S%26P_500_companies>`_.


This functionality is present in the ``companyList`` module. 
You can use the functionality as follows:

>>> import financeMacroFactors as fM
>>> companyList = fM.companies.getSNP500CompanyList()
>>> from pprint import pprint
>>> len(companyList)
505
>>> pprint(companyList[:3])
[{'CIK': '0000066740',
  'Date first added': '1976-08-09',
  'Founded': '1902',
  'GICS Sector': 'Industrials',
  'GICS Sub Industry': 'Industrial Conglomerates',
  'Headquarters Location': 'St. Paul, Minnesota',
  'SEC filings': 'reports',
  'Security': '3M Company',
  'Symbol': 'MMM'},
 {'CIK': '0000001800',
  'Date first added': '1964-03-31',
  'Founded': '1888',
  'GICS Sector': 'Health Care',
  'GICS Sub Industry': 'Health Care Equipment',
  'Headquarters Location': 'North Chicago, Illinois',
  'SEC filings': 'reports',
  'Security': 'Abbott Laboratories',
  'Symbol': 'ABT'},
 {'CIK': '0001551152',
  'Date first added': '2012-12-31',
  'Founded': '2013 (1888)',
  'GICS Sector': 'Health Care',
  'GICS Sub Industry': 'Pharmaceuticals',
  'Headquarters Location': 'North Chicago, Illinois',
  'SEC filings': 'reports',
  'Security': 'AbbVie Inc.',
  'Symbol': 'ABBV'}]
>>> 


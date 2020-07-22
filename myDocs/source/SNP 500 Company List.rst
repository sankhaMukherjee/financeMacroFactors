SNP 500 Company List
====================

An example of obtaining a list of companies that are in the SNP500.
The companies are obtained from the `wikipedia article
<https://en.wikipedia.org/wiki/List_of_S%26P_500_companies>`_.


This functionality is present in the ``companyList`` module. 
You can use the functionality as follows:

.. code-block:: python

    >> import financeMacroFactors as fM
    >> companyList = fM.companies.getSNP500CompanyList()
    >> print(companyList[:3])


This should result in a list of dictionaries as output as shown
below:

.. code-block:: python

    [{'Symbol': 'MMM', 'Security': '3M Company', 'SEC filings': 'reports', 'GICS Sector': 'Industrials', 'GICS Sub Industry': 'Industrial Conglomerates', 'Headquarters Location': 'St. Paul, Minnesota', 'Date first added': '1976-08-09', 'CIK': '0000066740', 'Founded': '1902'}, {'Symbol': 'ABT', 'Security': 'Abbott Laboratories', 'SEC filings': 'reports', 'GICS Sector': 'Health Care', 'GICS Sub Industry': 'Health Care Equipment', 'Headquarters Location': 'North Chicago, Illinois', 'Date first added': '1964-03-31', 'CIK': '0000001800', 'Founded': '1888'}, {'Symbol': 'ABBV', 'Security': 'AbbVie Inc.', 'SEC filings': 'reports', 'GICS Sector': 'Health Care', 'GICS Sub Industry': 'Pharmaceuticals', 'Headquarters Location': 'North Chicago, Illinois', 'Date first added': '2012-12-31', 'CIK': '0001551152', 'Founded': '2013 (1888)'}]
